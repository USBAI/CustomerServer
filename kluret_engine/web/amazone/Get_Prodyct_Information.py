import requests
from bs4 import BeautifulSoup

# URL of the Amazon product page
url = "https://www.amazon.se/Samsung-Galaxy-A04S-Android-black/dp/B0BFWXB5RC/ref=zg_mg_g_20637719031_d_sccl_4/257-2107428-9376105?psc=1"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the page content
response = requests.get(url, headers=headers)
if response.status_code == 200:
    page_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # Debug: Print the fetched HTML to a file to inspect it
    with open("fetched_page.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    # Extract the product title
    title_tag = soup.find('span', id='productTitle')
    title = title_tag.get_text(strip=True) if title_tag else "Title not found"

    # Extract the product price
    price_tag = soup.find('span', class_='aok-offscreen')
    price = price_tag.get_text(strip=True) if price_tag else "Price not found"

    # Extract the product technical details
    tech_details = {}
    tech_section = soup.find('table', id='productDetails_techSpec_section_1')
    if tech_section:
        rows = tech_section.find_all('tr')
        for row in rows:
            key = row.find('th').get_text(strip=True)
            value = row.find('td').get_text(strip=True)
            tech_details[key] = value
    else:
        tech_details = {"Error": "Technical details not found"}

    # Extract image links
    image_links = []
    image_list = soup.find_all('li', class_='a-spacing-small item imageThumbnail a-declarative')
    for img_tag in image_list:
        img = img_tag.find('img')
        if img and 'src' in img.attrs:
            image_links.append(img['src'])

    # Print extracted information
    print("Product Title:", title)
    print("Product Price:", price)
    print("Technical Information:")
    for key, value in tech_details.items():
        print(f"  {key}: {value}")
    print("Image Links:")
    for link in image_links:
        print(link)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
