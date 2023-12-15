
def normalize_file_name(input):
    output = input.replace('/', '_')
    output = output.replace(':', '_')
    output = output.replace('?', '_')
    output = output.replace('=', '_')
    output = output.replace('&', '_')
    output = output.replace('.', '_')
    return output

def get_links_a_tag(html_content, domain_url):
   
    visited_urls = set()
    # Find all the webpage links on the page
    links = html_content.find_all('a')
    
    # Extract the URLs from the links
    webpage_links = []
    other_links = []
    for link in links:
        if 'href' in link.attrs:
            href = link['href']
            if href.startswith('http') or href.startswith('https'):
                if href not in visited_urls:
                    visited_urls.add(href)
                    webpage_links.append(href)
            else:
                other_links.append(domain_url + href)
    
    # Combine webpage_links and other_links
    all_links = webpage_links + other_links
    
    return all_links, visited_urls
    