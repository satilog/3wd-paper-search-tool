import pandas as pd

from src.utils import save_to_csv


class PaperFilter:
    def __init__(self, config):
        self.filtered_results_file = config["output"]["filtered_results_file"]
        self.keywords_title = config["filter"]["keywords"]["title"]
        self.keywords_abstract = config["filter"]["keywords"]["abstract"]

    def filter_papers(self, papers):
        """Filter papers by keywords in title or abstract."""
        filtered = []
        for paper in papers:
            title = paper["Title"].lower()
            abstract = paper["Abstract"].lower()

            if any(kw in title for kw in self.keywords_title) or any(
                kw in abstract for kw in self.keywords_abstract
            ):
                filtered.append(paper)

        save_to_csv(filtered, self.filtered_results_file)
        return filtered
