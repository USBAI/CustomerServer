import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random
import string

def is_valid_url(url):
    """
    Check if a URL is valid.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def generate_random_string(length):
    """
    Generate a random string of specified length.
    """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def extract_product_details(url):
    """
    Extracts product name, price, color, description, and image URLs from the provided URL.
    Returns a dictionary with 'product_name', 'price', 'color', 'description', 'img_urls'.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product name
        product_name_elem = soup.find('h1', class_='sDq_FX')
        product_name = product_name_elem.text.strip() if product_name_elem else None

        # Extract price
        price_elem = soup.find('span', class_='sDq_FX _4sa1cA FxZV-M HlZ_Tf')
        price = price_elem.text.strip() if price_elem else None

        # Extract color
        color_elem = soup.find('span', class_='sDq_FX lystZ1 dgII7d HlZ_Tf zN9KaA')
        color = color_elem.get_text(strip=True) if color_elem else None

        # Extract description using the new logic
        description_elem = soup.find('div', class_='_5qdMrS VHXqc_ rceRmQ _4NtqZU mIlIve ypPCAR KwRvru DgFgr2')
        description = description_elem.get_text(separator=' ', strip=True) if description_elem else None

        # Extract image URLs, limit to between 2 to 5 images
        image_urls = []
        divs = soup.find_all('div', class_='KVKCn3 u-C3dd jDGwVr mo6ZnF KLaowZ')
        for div in divs:
            if len(image_urls) >= 5:
                break  # Limit reached, exit loop
            img_tag = div.find('img')
            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']
                image_urls.append(img_url)

        # Trim to a maximum of 5 images
        image_urls = image_urls[:5]

        # Generate a random product ID
        product_id = generate_random_string(random.randint(20, 50))

        # Construct the product details dictionary, excluding null/empty price and description
        product_details = {
            'category': 'Nordisk stil',
            'product_name': product_name,
            'color': color,
            'product_page': url,
            'product_id': product_id,
            'img_urls': image_urls
        }

        if price:
            product_details['price'] = price
        if description:
            product_details['description'] = description

        return product_details
    
    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {e}")
        return {
            'product_name': None,
            'price': None,
            'color': None,
            'description': None,
            'img_urls': [],
            'product_page': url,
            'product_id': None
        }

# Path to the product URLs JSON file
product_json_path = r"C:\Users\elias\OneDrive\Desktop\usbaiTraining\usbai_client\kluret_engine\web\zalando\pipline1\__link__\__link__2.json"

# Path to the pipeline JSON file
pipeline_json_path = r"C:\Users\elias\OneDrive\Desktop\usbaiTraining\usbai_client\kluret_engine\web\zalando\pipline1\pipline9.json"

# Initialize list to store product details
all_product_details = []

# Load URLs from product.json
try:
    with open(product_json_path, 'r') as file:
        product_urls = json.load(file)
except FileNotFoundError:
    print(f"Product JSON file not found at: {product_json_path}")
    product_urls = []

# Process each URL sequentially
for url in product_urls:
    if is_valid_url(url):
        product_details = extract_product_details(url)
        if product_details['product_name']:  # Only append valid product data
            # Save product details immediately to pipeline.json
            try:
                with open(pipeline_json_path, 'r') as file:
                    existing_data = json.load(file)
            except FileNotFoundError:
                existing_data = []

            existing_data.append(product_details)

            with open(pipeline_json_path, 'w') as file:
                json.dump(existing_data, file, indent=4)
                
            print(f"Product details appended to {pipeline_json_path} for URL: {url}")
        else:
            print(f"Skipping URL: {url} due to missing product name or other data")
    else:
        print(f"Invalid URL: {url}")

print("All URLs processed.")
