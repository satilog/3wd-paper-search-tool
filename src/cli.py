import os

import pandas as pd


class CLI:
    def __init__(self, all_results_file, filtered_results_file, pdf_download_folder):
        self.all_results_file = all_results_file
        self.filtered_results_file = filtered_results_file
        self.pdf_download_folder = pdf_download_folder

    def count_papers(self):
        """Count the number of papers in each stage."""
        all_results_count = 0
        filtered_results_count = 0
        downloaded_files_count = 0

        # Count all results
        if os.path.exists(self.all_results_file):
            all_results_count = len(pd.read_csv(self.all_results_file))

        # Count filtered results
        if os.path.exists(self.filtered_results_file):
            filtered_results_count = len(pd.read_csv(self.filtered_results_file))

        # Count downloaded PDFs
        if os.path.exists(self.pdf_download_folder):
            downloaded_files_count = len(
                [f for f in os.listdir(self.pdf_download_folder) if f.endswith(".pdf")]
            )

        return all_results_count, filtered_results_count, downloaded_files_count

    def display_status(self):
        """Display the status of papers in each stage."""
        all_results_count, filtered_results_count, downloaded_files_count = (
            self.count_papers()
        )
        print("\n--- Current Status ---")
        print(f"1. Papers retrieved in all_results.csv: {all_results_count}")
        print(f"2. Papers filtered in filtered_results.csv: {filtered_results_count}")
        print(f"3. Papers downloaded in filtered_papers/: {downloaded_files_count}")
        print("----------------------\n")

    def prompt_user_action(self):
        """Prompt the user to choose the next stage."""
        print("What would you like to do next?")
        print("1. Search for new papers")
        print("2. Filter existing list of papers")
        print("3. Download filtered papers")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()
        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            return self.prompt_user_action()

        return choice
