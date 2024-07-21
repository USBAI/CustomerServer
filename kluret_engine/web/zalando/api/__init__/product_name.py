import requests
from bs4 import BeautifulSoup

url = "https://www.zalando.se/bjoern-borg-essential-boxer-6-pack-underklaeder-black-bj282o0a5-q11.html"

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extracting the product name
product_name = soup.find('h1', class_='sDq_FX').text.strip()

# Extracting the price
price_element = soup.find('span', class_='sDq_FX _4sa1cA FxZV-M HlZ_Tf')
price = price_element.text.strip()

print("Product Name:", product_name)
print("Price:", price)
