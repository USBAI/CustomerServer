import requests
from bs4 import BeautifulSoup
import math
import time

# Correct Groq API endpoint (replace with the valid endpoint from documentation)
GROQ_API_URL = "https://api.groq.com/v1/query"  # Update this URL
GROQ_API_KEY = "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"

def fetch_page_html(url):
    """Fetch the HTML content of the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def split_html_into_chunks(html, chunk_size=5000):
    """Split the HTML into smaller chunks for processing."""
    return [html[i:i + chunk_size] for i in range(0, len(html), chunk_size)]

def query_groq(chunk, task_description):
    """Query the Groq API for a specific task."""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    payload = {
        "prompt": f"""
            Analyze the following HTML chunk. {task_description}
            HTML chunk:
            {chunk}
        """,
        "max_tokens": 500,
    }
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "").strip()
        else:
            print(f"Groq API error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error querying Groq API: {e}")
        return None

def process_html_with_agents(html_chunks):
    """Process HTML chunks with multiple AI agents."""
    tasks = [
        "Identify product information including names, prices, and images.",
        "Extract metadata like page titles, descriptions, and canonical URLs.",
        "Identify navigation links and categories.",
        "Detect any promotional content or banners on the page.",
        "Analyze the structure of the page to infer key sections like header, footer, and main content.",
    ]

    results = []
    for i, chunk in enumerate(html_chunks):
        for task in tasks:
            print(f"Processing chunk {i+1}/{len(html_chunks)} for task: {task}")
            result = query_groq(chunk, task)
            if result:
                results.append({"chunk": i+1, "task": task, "result": result})
            else:
                print(f"Task '{task}' failed for chunk {i+1}.")
            time.sleep(0.5)  # Rate-limiting to avoid API throttling

    return results

def main():
    print("Enter the URL of the webpage to analyze:")
    url = input().strip()

    print("Fetching page HTML...")
    html = fetch_page_html(url)
    if not html:
        return

    print("Splitting HTML into smaller chunks...")
    html_chunks = split_html_into_chunks(html)

    print("Processing HTML with AI agents...")
    results = process_html_with_agents(html_chunks)

    print("\nAggregated Results:\n")
    for result in results:
        print(f"Chunk {result['chunk']} - Task: {result['task']}")
        print(f"Result: {result['result']}\n")

if __name__ == "__main__":
    main()
