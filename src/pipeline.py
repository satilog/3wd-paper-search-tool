from src.search import PaperSearcher


class PaperSearchPipeline:
    def __init__(self, config):
        self.searcher = PaperSearcher(config)

    def run(self, search_term):
        print("Searching for papers...")
        papers = self.searcher.search_papers(search_term)
