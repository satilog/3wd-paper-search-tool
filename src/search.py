import time

from scholarly import scholarly

from src.utils import save_to_csv


class PaperSearcher:
    def __init__(self, config):
        self.config = config
        self.all_results_file = config["output"]["all_results_file"]
        self.max_results = config["search"]["max_results"]
        self.delay_seconds = config["general"]["delay_seconds"]

    def search_papers(self, search_term):
        """Search for papers and save results to a CSV."""
        search_results = scholarly.search_pubs(search_term)
        log_data = []

        for index, result in enumerate(search_results):
            paper_data = {
                "Title": result.get("bib", {}).get("title", "N/A"),
                "Authors": result.get("bib", {}).get("author", "N/A"),
                "Abstract": result.get("bib", {}).get("abstract", "N/A"),
                "Publication Year": result.get("bib", {}).get("pub_year", "N/A"),
                "Venue": result.get("bib", {}).get("venue", "N/A"),
                "Citations": result.get("num_citations", "N/A"),
                "URL": result.get("pub_url", "N/A"),
            }
            log_data.append(paper_data)
            save_to_csv([paper_data], self.all_results_file)

            if len(log_data) >= self.max_results:
                break

            time.sleep(self.delay_seconds)
        return log_data
