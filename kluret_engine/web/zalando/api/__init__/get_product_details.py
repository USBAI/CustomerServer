import requests
from bs4 import BeautifulSoup

# Define the URL of the webpage
url = 'https://www.zalando.se/clean-cut-copenhagen-patrick-t-shirt-med-print-black-c6v22o00a-q11.html'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the specified div and count the number of <li> elements within it
    div_class = 'XLgdq7 _0xLoFW JgpeIw r9BRio be4rWJ xlsKrm _4oK5GO I7OI1O C3wGFf AEfWtw _0xLoFW be4rWJ heWLCX sKmkSN pMa0tB'
    ul_tag = soup.find('ul', class_=div_class)
    li_count = len(ul_tag.find_all('li')) if ul_tag else 4
    
    # Extract image URLs from the specified div
    image_urls = []
    divs = soup.find_all('div', class_='KVKCn3 u-C3dd jDGwVr mo6ZnF KLaowZ')
    for div in divs:
        img_tag = div.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            image_urls.append(img_url)
    
    # Print image URLs up to the number of <li> elements or a maximum of 10
    max_print = min(li_count, 10)
    for img_url in image_urls[:max_print]:
        print(img_url)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
