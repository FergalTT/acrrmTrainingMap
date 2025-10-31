#!/usr/bin/env python3
"""Test scraper on first 3 pages"""

import sys
sys.path.insert(0, '/Users/fergaltemple')

from scrape_acrrm import fetch_page, parse_page
import json

print("Testing scraper on first 3 pages...")

for page_num in [1, 2, 3]:
    print(f"\n=== Page {page_num} ===")
    html = fetch_page(page_num)
    posts = parse_page(html)
    print(f"Found {len(posts)} posts")

    if posts:
        print("\nFirst post:")
        print(json.dumps(posts[0], indent=2))

print("\nTest complete!")
