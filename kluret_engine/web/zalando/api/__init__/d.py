import requests
from bs4 import BeautifulSoup

# URL of the page
url = "https://www.zalando.se/only-and-sons-onsneil-karl-mid-thigh-shorts-cloud-dancer-os322f0fv-a11.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specific <div> with the given class
    target_div = soup.find('div', class_='_5qdMrS VHXqc_ rceRmQ _4NtqZU mIlIve ypPCAR KwRvru DgFgr2')

    if target_div:
        # Extract text from the specific <div>
        div_text = target_div.get_text(separator=' ', strip=True)
        print(div_text)
    else:
        print("The specified <div> was not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
