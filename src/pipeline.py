from src.download import PDFDownloader
from src.filter import PaperFilter
from src.search import PaperSearcher


class PaperSearchPipeline:
    def __init__(self, config):
        self.searcher = PaperSearcher(config)
        self.filter = PaperFilter(config)
        self.downloader = PDFDownloader(config)

    def run(self, search_term):
        print("Searching for papers...")
        papers = self.searcher.search_papers(search_term)

        print("Filtering papers...")
        filtered_papers = self.filter.filter_papers(papers)

        print("Downloading PDFs...")
        self.downloader.download_pdfs(filtered_papers)
