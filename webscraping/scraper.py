import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
import sys

sys.path.insert(0, '../utils')
from utils.content_util import normalize_file_name, get_links_a_tag

visited_urls = set()
processed_links = set()

def get_links(url, domain):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        content = BeautifulSoup(response.content, 'html.parser')
       
        all_links, visited_urls = get_links_a_tag(content, domain)        # webpage_links = []
    
        visited_urls = visited_urls.union(visited_urls)
        return all_links
    else:
        print('Failed to retrieve data from the URL.')


def get_content(link):
    response = requests.get(link)
    if response.status_code == 200:
        # Normalize the URL to use as the file name
        file_name = os.path.basename(link)
        file_name = normalize_file_name(file_name) + '.txt'

        # Create the content folder if it doesn't exist
        if not os.path.exists('content'):
            os.makedirs('content')

        # Write the content to a text file in the content folder
        with open(os.path.join('content', file_name), 'wb') as file:
            file.write(response.content)
    else:
        print(f'Failed to retrieve data from {link}')


def process_links(url, domain):
    webpage_links = get_links(url, domain)
    if webpage_links:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(get_content, webpage_links)
        for link in webpage_links:
            process_links(link, domain)
            processed_links.add(link)


# Example usage
url = 'https://retool.com/'
domain = "https://retool.com"
visited_urls.add(url)
process_links(url, domain)
