import argparse

import pandas as pd
import yaml

from src.cli import CLI
from src.pipeline import PaperSearchPipeline
from src.search import PaperSearcher


def main():
    parser = argparse.ArgumentParser(description="Paper Search Tool")
    parser.add_argument(
        "--config",
        type=str,
        default="./config/config.yaml",
        help="Path to the config file",
    )
    args = parser.parse_args()

    # Load configuration
    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

    all_results_file = config["output"]["all_results_file"]
    filtered_results_file = config["output"]["filtered_results_file"]
    pdf_download_folder = config["download"]["pdf_folder"]

    # Initialize CLI and display current status
    cli = CLI(all_results_file, filtered_results_file, pdf_download_folder)
    cli.display_status()

    # Prompt user for next action
    choice = cli.prompt_user_action()

    # Initialize pipeline components
    searcher = PaperSearcher(config)

    # Execute based on user choice
    if choice == "1":
        search_term = input("Enter the search term: ").strip()
        searcher.search_papers(search_term)
    elif choice == "2":
        print("Filtering existing list of papers...")
        all_papers = pd.read_csv(all_results_file).to_dict(orient="records")
        print("TODO")
    elif choice == "3":
        print("Downloading filtered papers...")
        filtered_papers = pd.read_csv(filtered_results_file).to_dict(orient="records")
        print("TODO")
    elif choice == "4":
        print("Exiting the tool.")
        return


if __name__ == "__main__":
    main()
