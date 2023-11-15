# arXiv Papers Scraper

## Overview
This Python script is designed to scrape research papers from arXiv based on specified search queries. It utilizes the arXiv API to retrieve information about academic papers, such as titles, authors, abstracts, and download links, and organizes the downloaded papers into folders based on publication date and category.

## Usage
To use this script, follow these steps:

1. **Install Dependencies:** Make sure you have the required Python packages installed. You can install them using the following command:
    ```bash
    pip install beautifulsoup4 requests pandas numpy lxml tqdm
    ```

2. **Run the Script:** Execute the script using a Python interpreter. Ensure that the script file (`arxiv_scraper.py`) is in the same directory as the `objects.py` and `utils.py` files.
    ```bash
    python arxiv_scraper.py
    ```

3. **Check Output:** The script will create a directory named `Papers-%Y-%m-%d %H-%M-%S`, where `%Y-%m-%d %H-%M-%S` is the current date and time. Inside this directory, you'll find subdirectories containing downloaded papers organized by publication date and category.

4. **Log Information:** The script generates a log file (`log.csv`) containing information about the downloaded papers, including the publication date, category, and the number of papers in each category.

## Configuration
You can customize the script by modifying the following sections:

### Search Query and Options
Adjust the `qs` (query strings) and `options` lists to specify your search criteria. The script currently includes example queries for searching papers related to "Interpolation" in the computer science category.

### Output Directory
By default, the script creates a directory named `Papers-%Y-%m-%d %H-%M-%S`. You can customize the `save_path` variable in the script to change the output directory name.

### File Naming and Organization
The script organizes downloaded papers into folders based on publication date and category. You can customize the file naming and organization logic by modifying the relevant sections in the script.

## Notes
- The script uses the arXiv API to fetch paper information. Ensure that your system has internet access and can connect to the arXiv API (`http://export.arxiv.org`).
- The script requires writing permissions to the current working directory to create the output directory and log files.

## Disclaimer
This script is provided as-is, and the user is responsible for adhering to the terms of service of the arXiv API and respecting copyright and licensing restrictions for the downloaded papers. The script is intended for educational and research purposes.