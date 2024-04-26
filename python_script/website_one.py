"""
Script to scrape a Bid Solicitation informations from a website, saves the data to a JSON file, and downloads the associated documents to a specified folder

Dependencies:
- requests
- BeautifulSoup (bs4)
- tqdm
- Path (pathlip)
- re
- Json

Usage:
1. Run the script to scrape Bid Solicitation informations from the specified URL.
2. The scraped data will be saved to a json file and saved the documents to the specified folder path.

"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm
import re
import json

# Folder path where documents will be saved
SAVE_DOCUMENTS_PATH = 'D:\VinothOfficial\catalyst_partners\save_documents'

#File path to save json file
SAVE_JSON_PATH = 'D:\VinothOfficial\catalyst_partners\output_files\website_one_json.json'

def get_number(strng):
    """Extract the first number from a string using regular expression."""
    return re.findall(r'\d+', strng)[0]

def clean_string(strng):
    """Clean up a string by removing newline, tab characters, and leading/trailing whitespaces."""
    return strng.replace('\n', '').replace('\t', '').strip()

def get_post_response(url, payload, headers):
    """Send a POST request and return the response."""
    response = requests.post(url, headers=headers, data=payload)
    return response

def download_document(link, bid_solicitation_number, document_id):
    """Download a document from a given link and save it to the specified folder path."""

    url = document_url
    payload = f"_csrf={str(cookie_dict['XSRF-TOKEN'])}&mode=download&bidId={bid_solicitation_number}&docId={bid_solicitation_number}&currentPage=1&querySql=&downloadFileNbr={document_id}&itemNbr=undefined&parentUrl=close&fromQuote=&destination="
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Referer': str(link),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36:'
    }
    response = get_post_response(url, payload, headers)
    Path(f'{SAVE_DOCUMENTS_PATH}{bid_solicitation_number}').mkdir(parents=True, exist_ok=True)
    file_name = f'{SAVE_DOCUMENTS_PATH}{bid_solicitation_number}\\{document_id}.pdf'
    with open(file_name, 'wb') as f:
        f.write(response.content)
        print(f'Document saved at: {file_name}')

def get_header_information(next_link, bid_solicitation_number):
    """Get header information from the next link."""

    url = next_link
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.content, "lxml")
    tables = soup.find_all('table', {'class': 'table-01'})[0].find_all('table')[0]
    trs = tables.find_all('tr')
    header_info = {}
    for tr in trs:
        tds = tr.find_all('td', {'class': 't-head-01'})
        for td in tds:
            head = clean_string(str(td.get_text()))
            if 'File Attachments' not in head:
                header_info[head] = clean_string(str(td.find_next_sibling('td').get_text()))
            else:
                file_numbers = td.find_next_sibling('td').find_all('a')
                file_ids = []
                for filenumber in file_numbers:
                    file_id = get_number(str(filenumber['href']))
                    download_document(next_link, bid_solicitation_number, file_id)
                    file_ids.append(file_id)
                header_info[head] = file_ids
    return header_info

def parse(response):
    """Parse the response and extract information."""

    bid_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        trs = soup.find_all('tr')
        for tr in tqdm(trs):
            bid_info = {}
            tds = tr.find_all('td')
            bid_info['bid_solicitation'] = tds[0].get_text()
            bid_info['next_link'] = "https://nevadaepro.com" + str(tds[0].find('a')['href'])
            bid_info['buyer'] = tds[5].get_text()
            bid_info['description'] = tds[6].get_text()
            bid_info['bid_openingdate'] = tds[7].get_text()
            bid_info['header_information'] = get_header_information(bid_info['next_link'], bid_info['bid_solicitation'])
            bid_list.append(bid_info)
        return bid_list 
    else:
        print('Failed to get response')
        return bid_list 

def save_to_json(bid_data, file_path):
    """Save the list of dictionaries to a json file."""
    
    with open(file_path, "w") as final:
        json.dump(bid_data, final)
    print(f"Data saved to Json: {file_path}")

def get_cookie_info(url):
    """Get cookie information from the URL."""

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.content, "lxml")
    view_state = soup.find('input', {'name': 'javax.faces.ViewState'})['value']
    total_page = int(soup.find('span', {'class': 'ui-paginator-pages'}).find_all('span')[-1].get_text())
    cookie_dict = {}
    for cookies in response.cookies:
        cookie_dict[cookies.name] = cookies.value
    return cookie_dict, view_state, total_page

if __name__ == '__main__':
    initial_url = 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true'
    data_url = "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml"
    document_url = "https://nevadaepro.com/bso/external/bidDetail.sdo"

    cookie_dict, view_state, total_page = get_cookie_info(initial_url)
    
    cookie = f'JSESSIONID={str(cookie_dict['JSESSIONID'])}; XSRF-TOKEN={str(cookie_dict['XSRF-TOKEN'])}; dtCookie={str(cookie_dict['dtCookie'])}; AWSALB={str(cookie_dict['AWSALB'])}; AWSALBCORS={str(cookie_dict['AWSALBCORS'])}'

    page = 0
    bid_data = []
    for i in tqdm(range(1, total_page + 1)):
        payload = f"javax.faces.partial.ajax=true&javax.faces.source=bidSearchResultsForm%3AbidResultId&javax.faces.partial.execute=bidSearchResultsForm%3AbidResultId&javax.faces.partial.render=bidSearchResultsForm%3AbidResultId&bidSearchResultsForm%3AbidResultId=bidSearchResultsForm%3AbidResultId&bidSearchResultsForm%3AbidResultId_pagination=true&bidSearchResultsForm%3AbidResultId_first={str(page)}&bidSearchResultsForm%3AbidResultId_rows=25&bidSearchResultsForm%3AbidResultId_encodeFeature=true&bidSearchResultsForm=bidSearchResultsForm&_csrf={str(cookie_dict['XSRF-TOKEN'])}&openBids=true&javax.faces.ViewState={str(view_state)}"
        
        headers = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ta;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cookie,
            'Referer': initial_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        response = get_post_response(data_url, payload, headers)
        bid_data.extend(parse(response))
        page = page + 25

    save_to_json(bid_data, SAVE_JSON_PATH)
