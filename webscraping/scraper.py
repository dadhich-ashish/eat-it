import requests
from bs4 import BeautifulSoup
import os

def get_links(url, domain):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the webpage links on the page
        links = soup.find_all('a')
       
        # Extract the URLs from the links
        webpage_links = []
        other_links = []
        for link in links:
            if 'href' in link.attrs:
                href = link['href']
                if href.startswith('http') or href.startswith('https'):
                    webpage_links.append(href)
                else:
                    other_links.append(domain + href)
        
        # Combine webpage_links and other_links
        all_links = webpage_links + other_links
        
        return all_links
    else:
        print('Failed to retrieve data from the URL.')


def get_content(webpage_links):
    # Create the content folder if it doesn't exist
    if not os.path.exists('content'):
        os.makedirs('content')

    # Get the content of each webpage link
    webpage_content = {}
    for link in webpage_links:
        response = requests.get(link)
        if response.status_code == 200:
            webpage_content[link] = response.content
            # Normalize the URL to use as the file name
            file_name = os.path.basename(link)
            file_name = file_name.replace('/', '_')
            file_name = file_name.replace(':', '_')
            file_name = file_name.replace('?', '_')
            file_name = file_name.replace('=', '_')
            file_name = file_name.replace('&', '_')
            file_name = file_name.replace('.', '_')
            file_name = file_name + '.txt'
            # Write the content to a text file in the content folder
            with open(os.path.join('content', file_name), 'wb') as file:
                file.write(response.content)
        else:
            print(f'Failed to retrieve data from {link}')

    #print(webpage_content)

# Example usage
url = 'https://pypi.org/project/project-generator/'
webpage_links = get_links(url, "https://pypi.org")

get_content(webpage_links)
