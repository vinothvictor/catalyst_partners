"""
Script to scrape a staff directory from a website and save the data to a CSV file.

Dependencies:
- requests
- BeautifulSoup (bs4)
- tqdm
- pandas

Usage:
1. Run the script to scrape the staff directory from the specified URL.
2. The scraped data will be saved to a CSV file at the specified file path.

"""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


#File path to save json file
SAVE_CSV_PATH = 'D:\VinothOfficial\catalyst_partners\output_files\website_two_csv.csv'

def clean_string(strng):
    """Clean up a string by removing newline, tab characters, and leading/trailing whitespaces."""

    return strng.replace('\n', '').replace('\t', '').strip()

def get_common_details(html_content):
    """Extract common details like school name, address, state, and zip code from the HTML content."""
    
    common_fields = {}
    soup = BeautifulSoup(html_content, "lxml")
    school_name = soup.find('div', {'class': 'site-name'}).get_text()
    address_details = soup.find('div', {'class': 'field location label-above'}).find('p').get_text()
    address = address_details.strip().split('\n')[0].strip()
    state = address_details.strip().split('\n')[1].split(',')[0].strip()
    zip_code = address_details.strip().split('\n')[1].split(',')[-1].strip()
    total_page = int(soup.find('li', {'class': 'item last'}).find('a')['href'].split('=')[-1])
    common_fields = {'school_name': school_name, 'address': address, 'state': state, 'zip_code': zip_code}
    return common_fields, total_page

def parse(html_content, common_fields):
    """Parse the HTML content to extract staff information."""
    
    soup = BeautifulSoup(html_content, "lxml")
    staff_list = []
    for div_tag in soup.find_all('div', {'class': 'views-row'}):
        staff_info={}
        name = clean_string(div_tag.find('h2').get_text())
        first_name, last_name = map(clean_string, name.split(','))
        staff_info = {
            'school_name': clean_string(common_fields['school_name']),
            'address': clean_string(common_fields['address']),
            'state': clean_string(common_fields['state']),
            'zip_code': clean_string(common_fields['zip_code']),
            'first_name': clean_string(first_name),
            'last_name': clean_string(last_name),
            'title': clean_string(div_tag.find('div', {'class': 'field job-title'}).get_text()),
            'Phone': clean_string(div_tag.find('div', {'class': 'field phone'}).get_text()),
            'email': clean_string(div_tag.find('div', {'class': 'field email'}).get_text())
        }
        staff_list.append(staff_info)
    return staff_list

def save_to_csv(staff_data, file_path):
    """Save the list of dictionaries to a CSV file."""
    
    df = pd.DataFrame(staff_data)
    df.to_csv(file_path, index=False)
    print(f"Data saved to CSV: {file_path}")
    
def scrape_staff_directory(url, file_path):
    """Scrape the staff directory from the specified URL and save the data to a CSV file."""
    initial_response = requests.get(url)
    common_fields, total_page = get_common_details(initial_response.content)
    staff_data = []
    for page in tqdm(range(total_page + 1)):
        page_url = f"{url}?s=&page={page}"
        print(f"Scraping page {page}: {page_url}")
        response = requests.get(page_url)
        staff_data.extend(parse(response.content, common_fields))
    save_to_csv(staff_data, file_path)
    

if __name__ == '__main__':
    url = "https://isd110.org/our-schools/laketown-elementary/staff-directory"
    scrape_staff_directory(url, SAVE_CSV_PATH)
