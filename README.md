# catalyst_partners

1. Website 1

Website to be scrapped - https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true

Bid Solicitation Scraper
This Python script scrapes bid solicitation information from a website, saves the data to a JSON file, and downloads the associated documents to a specified folder.

Dependencies
    requests
    BeautifulSoup (bs4)
    tqdm
    Path (pathlib)
    re
    Json

Usage
    1. Install the required dependencies using pip:
        pip install requests beautifulsoup4 tqdm Json

    2. Modify the script to specify the folder path where documents will be saved (SAVE_DOCUMENTS_PATH) and the file path to save the JSON file (SAVE_JSON_PATH).

    3. Run the script using the following command:
        python website_one.py

Functionality
    The script sends a POST request to a specified URL to scrape bid solicitation information.
    It extracts bid details such as solicitation number, buyer, description, and bid opening date.
    For each bid, it retrieves additional header information from the next link and downloads associated documents.
    It extracts data for all existing pages
    The scraped data is saved to a JSON file (website_one_json.json) and documents are saved to the specified folder path (save_documents).
    
Note
    Ensure that the folder path where documents will be saved exists before running the script.

###############################################################################################################################################################################

2. Website 2

Website to be scrapped -  https://isd110.org/our-schools/laketown-elementary/staff-directory

Staff Directory Scraper
This Python script scrapes a staff directory from a website and saves the data to a CSV file.

Dependencies
    requests
    BeautifulSoup (bs4)
    tqdm
    pandas

Usage
    1. Install the required dependencies using pip:
        pip install requests beautifulsoup4 tqdm pandas

    2. Modify the script to specify the URL of the staff directory (url) and the file path to save the CSV file (SAVE_CSV_PATH).

    3. Run the script using the following command:
        python website_two.py

Functionality
    The script sends a GET request to the specified URL to retrieve the HTML content of the staff directory.
    It extracts common details like school name, address, state, and zip code from the HTML content.
    The script then parses the HTML content to extract staff information such as name, title, phone, and email for all pages.
    The scraped data is saved to a CSV file (website_two_csv.csv) at the specified file path.

Notes
    Modify the file path (SAVE_CSV_PATH) to specify where the CSV file will be saved.
    Additional modifications may be required based on the structure of the staff directory page.