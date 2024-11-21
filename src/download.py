import os

import requests


class PDFDownloader:
    def __init__(self, config):
        self.pdf_folder = config["download"]["pdf_folder"]

    def download_pdfs(self, papers):
        """Download PDFs for filtered papers with progress tracking."""
        os.makedirs(self.pdf_folder, exist_ok=True)
        total_papers = len(papers)
        downloaded_count = 0
        failed_count = 0

        for index, paper in enumerate(papers, start=1):
            url = paper.get("URL", "N/A")
            title = paper.get("Title", "N/A")
            if url == "N/A":
                print(f"[{index}/{total_papers}] Skipping {title}: No URL provided.")
                failed_count += 1
                continue

            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                file_path = os.path.join(self.pdf_folder, f"{title}.pdf")
                with open(file_path, "wb") as file:
                    file.write(response.content)
                downloaded_count += 1
                print(f"[{index}/{total_papers}] Successfully downloaded: {title}")
            except Exception as e:
                failed_count += 1
                print(f"[{index}/{total_papers}] Failed to download {title}: {e}")

        # Summary log
        print("\n--- Download Summary ---")
        print(f"Total papers: {total_papers}")
        print(f"Successfully downloaded: {downloaded_count}")
        print(f"Failed downloads: {failed_count}")
        print("------------------------")
