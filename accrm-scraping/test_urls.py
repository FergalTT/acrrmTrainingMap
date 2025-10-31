#!/usr/bin/env python3
"""Test different URL patterns"""

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Try different URLs
urls_to_test = [
    "https://mycollege.acrrm.org.au/search/find-training-post",
    "https://mycollege.acrrm.org.au/search/find-training-post?start_rank=11",
    "https://mycollege.acrrm.org.au/search/find-teaching-post",
    "https://mycollege.acrrm.org.au/search/find-teaching-post?start_rank=11",
    "https://mycollege.acrrm.org.au/search/find-training-post?query=&collection=acrrm-fatp-public&start_rank=11",
]

for url in urls_to_test:
    print(f"\nTesting: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"  Status: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        containers = soup.find_all('div', class_='srContainer')
        print(f"  Found {len(containers)} result containers")

        if containers:
            first_title = containers[0].find('div', class_='srTitle')
            if first_title:
                print(f"  First result: {first_title.get_text(strip=True)[:60]}")

    except Exception as e:
        print(f"  Error: {e}")
