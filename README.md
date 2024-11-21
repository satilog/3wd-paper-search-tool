# 3WD Paper Search Tool

# Three Way Decisions in Intrusion Detection Systems (IDS)

## Overview

This repository contains a Python-based application that streamlines the research and analysis of scholarly papers focusing on the application of Three Way Decisions (TWD) in Intrusion Detection Systems (IDS). The project provides tools to search for, download, analyze, and extract insights from research papers. It also highlights the practical implications of TWD in improving the effectiveness of IDS in cybersecurity.

## Key Features

- **Search and Retrieval**: Automatically searches for research papers from platforms like Google Scholar using specific keywords.
- **PDF Download**: Downloads PDFs of research papers from search results, ensuring valid file formats.
- **Knowledge Extraction**: Extracts key information from the PDFs using OpenAI’s API and generates structured JSON outputs.
- **Merged Insights**: Combines metadata from search results and extracted knowledge for deeper analysis.
- **Statistics Dashboard**: Displays detailed statistics about downloaded and analyzed papers, including keyword matches and file counts.
- **Interactive CLI**: Provides a user-friendly command-line interface for managing tasks like searching, downloading, and extracting knowledge.

## Project Structure

The folder structure for this project is as follows:

```
3wd-paper-search-tool/
│
├── config/
│   └── config.yaml            # Configuration file for the application
│
├── data/                      # Directory for storing downloaded and processed data
│   └── (ignored by .gitignore)
│
├── data_backup/               # Backup directory for data (ignored by .gitignore)
│
├── src/                       # Source code directory
│   ├── pycache/           # Cached Python files (ignored by .gitignore)
│   ├── prompts/               # Prompt definitions for LLM
│   │   └── llm_prompt.py      # LLM-specific prompt generator
│   ├── cli.py                 # Command-line interface logic
│   ├── download.py            # Handles downloading of papers
│   ├── filter.py              # Logic for filtering research papers
│   ├── knowledge_extractor.py # LLM-based knowledge extraction logic
│   ├── pipeline.py            # Workflow orchestration
│   ├── search.py              # Paper search logic using Selenium
│   └── utils.py               # Utility functions for the project
│
├── .env                       # Environment file for storing secrets (ignored by .gitignore)
├── .gitignore                 # Specifies files and folders to be ignored by Git
├── environment.yaml           # Conda environment configuration
├── makefile                   # Makefile for setting up and running the project
└── main.py                    # Entry point of the application
```

## Ignored Files and Folders

The following files and directories are ignored using `.gitignore`:

- `.env`
- `data/`
- `data_backup/`
- `__pycache__/`

## Features

1. **Paper Search**:
   - Searches for research papers based on a given search term using Selenium.
   - Results are saved to `search_results.csv`.

2. **PDF Download**:
   - Downloads papers as PDFs from URLs present in `search_results.csv`.
   - Ensures file safety and tracks failed downloads.

3. **Knowledge Extraction**:
   - Extracts structured knowledge from the downloaded PDFs using an LLM.
   - Saves individual JSON files for each paper and a merged JSON file.

4. **Command-Line Interface**:
   - Provides a CLI to navigate through the workflow, check statistics, and perform specific tasks.

## Usage

1. **Setup**:
   - Install dependencies: `conda env create -f environment.yaml`
   - Activate the environment: `conda activate paper_search_tool`

2. **Run the Application**:
   - Use the command: `python main.py`

3. **Commands**:
   - `Search for new papers and download PDFs`
   - `Download papers from search_results.csv`
   - `Extract knowledge for downloaded papers`
   - `View statistics`

## Contributions

Contributions are welcome! Please ensure all PRs adhere to the project structure and coding standards.

## License

This project is licensed under the [MIT License](LICENSE).