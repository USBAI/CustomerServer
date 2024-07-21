import requests
from bs4 import BeautifulSoup
import json
import re

def extract_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product ID
    productID = re.search(r'/dp/(.*?)/', url).group(1)

    # Extract title
    title_elem = soup.find('span', {'id': 'productTitle'})
    if title_elem:
        title = title_elem.text.strip()
    else:
        title = None

    # Extract price
    price_elem = soup.find('span', {'id': 'priceblock_ourprice'})
    if price_elem:
        price = price_elem.text.strip()
    else:
        price = None

    # Extract technical information
    tech_info = {}
    tech_info_table = soup.find('table', {'id': 'productDetails_techSpec_section_1'})
    if tech_info_table:
        rows = tech_info_table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 2:
                key = columns[0].text.strip()
                value = columns[1].text.strip()
                tech_info[key] = value

    # Extract image links
    imageLinks = []
    image_links = soup.find_all('img', {'data-old-hires': True})
    for img in image_links:
        img_url = img.get('data-old-hires')
        if img_url:
            imageLinks.append(img_url)

    product_data = {
        "productID": productID,
        "title": title,
        "price": price,
        "technicalInformation": tech_info,
        "imageLinks": imageLinks
    }

    return product_data

# List of Amazon product URLs
urls = [
    "https://www.amazon.se/Apple-iPhone-Pro-Max-256/dp/B0BDKFJXCB/ref=zg_mg_g_20637719031_d_sccl_1/259-9461241-5321128?psc=1",
    "https://www.amazon.se/OnePlus-Nord-5G-SIM-fri-Smartphone/dp/B0C5F334B3/ref=zg_mg_g_20637719031_d_sccl_2/259-9461241-5321128?psc=1",
    # Add more URLs here
]

# Extract data for each URL
all_products_data = []
for url in urls:
    product_data = extract_product_details(url)
    if product_data:
        all_products_data.append(product_data)

# Save all products data to a JSON file
output_file = 'amazon_products.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_products_data, f, indent=4, ensure_ascii=False)

print(f"Data saved to {output_file}")
