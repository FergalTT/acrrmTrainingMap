#!/usr/bin/env python3
"""Test the scraper on first page only"""

import requests
from bs4 import BeautifulSoup
import json

url = "https://mycollege.acrrm.org.au/search/find-training-post"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

print("Fetching first page...")
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

soup = BeautifulSoup(response.text, 'html.parser')

# Save HTML for inspection
with open('/Users/fergaltemple/page_source.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("HTML saved to page_source.html")

# Try to find result cards/containers
print("\n=== Looking for result containers ===")

# Try various common class names
possible_containers = [
    'result',
    'card',
    'training-post',
    'search-result',
    'post-item',
]

for container in possible_containers:
    elements = soup.find_all(class_=lambda x: x and container in x.lower())
    if elements:
        print(f"Found {len(elements)} elements with '{container}' in class")

# Try finding by ID
results_div = soup.find(id=lambda x: x and 'result' in x.lower())
if results_div:
    print(f"Found results div by ID: {results_div.get('id')}")

# Look for the total count
total_elem = soup.find(text=lambda x: x and '1,174' in str(x))
if total_elem:
    print(f"Found total count text: {total_elem.strip()}")

# Try to find any h3 or h4 tags (likely post titles)
titles = soup.find_all(['h3', 'h4'])
print(f"\nFound {len(titles)} h3/h4 elements")
if titles:
    print("First few titles:")
    for i, title in enumerate(titles[:5]):
        print(f"  {i+1}. {title.get_text(strip=True)[:80]}")

print("\nDone!")
