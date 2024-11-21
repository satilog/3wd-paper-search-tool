import os
import re
import time
from collections import Counter, defaultdict

import pandas as pd
import requests
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.utils import save_to_csv


class PaperSearch:
    def __init__(self, config):
        self.config = config
        self.search_results_file = config["search"]["output"]
        self.pdf_folder = config["download"]["pdf_folder"]
        self.keywords_title = config["search"]["filter"]["keywords"]["title"]
        self.keywords_abstract = config["search"]["filter"]["keywords"]["abstract"]
        self.max_results = config["search"]["max_results"]
        self.delay = config["search"]["delay"]

        # Initialize Selenium WebDriver with options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

        # Ensure the PDF folder exists
        os.makedirs(self.pdf_folder, exist_ok=True)

    @staticmethod
    def generate_paper_id(title):
        """Generate a file name-safe paper ID from the title."""
        return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")

    def download_pdf(self, url, paper_id):
        """Download the PDF file for a paper."""
        if not url or ".pdf" not in url.lower():
            print(f"Skipping {paper_id}: URL does not point to a PDF file.")
            return False
        try:
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()
            file_path = os.path.join(self.pdf_folder, f"{paper_id}.pdf")
            with open(file_path, "wb") as file:
                file.write(response.content)
            return True
        except Exception as e:
            print(f"Failed to download PDF for {paper_id}: {e}")
            return False

    def search_papers(self, search_term):
        """Search, filter, and download papers in a single process."""
        if os.path.exists(self.search_results_file):
            print(
                f"Search results file '{self.search_results_file}' already exists. Skipping search."
            )
            return

        search_url = (
            f"https://scholar.google.com/scholar?q={search_term.replace(' ', '+')}"
        )
        self.driver.get(search_url)
        time.sleep(2)

        log_data = []
        total_results = 0

        print("\nSearching, filtering, and downloading papers...")
        while total_results < self.max_results:
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3.gs_rt a")
            if not results:
                print("No results found on this page. Exiting.")
                break

            for result in results:
                if total_results >= self.max_results:
                    break

                try:
                    title = result.text
                    url = result.get_attribute("href")
                    parent = result.find_element(
                        By.XPATH, "./ancestor::div[@class='gs_ri']"
                    )
                    authors_and_year = parent.find_element(
                        By.CSS_SELECTOR, ".gs_a"
                    ).text
                    abstract = parent.find_element(By.CSS_SELECTOR, ".gs_rs").text

                    # Extract authors and year
                    authors = "N/A"
                    year = "N/A"
                    if authors_and_year:
                        authors_split = authors_and_year.split("-")[0].strip()
                        year_split = authors_and_year.split(",")[-1].strip()
                        authors = authors_split if authors_split else "N/A"
                        year = year_split if year_split.isdigit() else "N/A"

                    # Generate a paper ID
                    paper_id = self.generate_paper_id(title)

                    # Check for keyword matches
                    matches_title = [
                        kw for kw in self.keywords_title if kw in title.lower()
                    ]
                    matches_abstract = [
                        kw for kw in self.keywords_abstract if kw in abstract.lower()
                    ]
                    matched_keywords = set(matches_title + matches_abstract)

                    # Prepare log entry
                    paper_data = {
                        "Title": title,
                        "Authors": authors,
                        "Abstract": abstract,
                        "Publication Year": year,
                        "Venue": "Google Scholar",
                        "Citations": "N/A",
                        "URL": url,
                        "paper_id": paper_id,
                        "Keywords Matched": ", ".join(matched_keywords),
                        "Download Failed": False,
                    }

                    # Download the PDF if keywords matched
                    if matched_keywords:
                        success = self.download_pdf(url, paper_id)
                        paper_data["Download Failed"] = not success
                        if success:
                            total_results += 1
                            print(f"Downloaded: {title}")

                    # Save the paper data to the CSV
                    save_to_csv([paper_data], self.search_results_file)
                    log_data.append(paper_data)

                except Exception as e:
                    print(f"Error processing result: {e}")

            # Move to the next page
            try:
                next_button = self.driver.find_element(By.LINK_TEXT, "Next")
                next_button.click()
                time.sleep(self.delay)
            except Exception:
                print(
                    "No more pages to load or 'Next' button unavailable. Ending search."
                )
                break

        self.driver.quit()
        print("\nSearch, filter, and download process completed.")
        return log_data

    def get_stats(self):
        """Generate keyword combination statistics from the search results."""
        if not os.path.exists(self.search_results_file):
            print(f"Search results file '{self.search_results_file}' not found.")
            return

        # Load search results
        search_results = pd.read_csv(self.search_results_file)
        combination_stats = defaultdict(lambda: {"Title": 0, "Abstract": 0, "Total": 0})

        for _, row in search_results.iterrows():
            keywords = row["Keywords Matched"].split(", ")
            for keyword in keywords:
                if keyword:
                    if keyword in row["Title"].lower():
                        combination_stats[keyword]["Title"] += 1
                    if keyword in row["Abstract"].lower():
                        combination_stats[keyword]["Abstract"] += 1
                    combination_stats[keyword]["Total"] += 1

        # Display stats in a table
        table = PrettyTable(
            ["Keyword", "Matches in Title", "Matches in Abstract", "Total Matches"]
        )
        for keyword, stats in combination_stats.items():
            table.add_row([keyword, stats["Title"], stats["Abstract"], stats["Total"]])

        print("\n--- Keyword Combination Statistics ---")
        print(table)
