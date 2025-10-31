#!/usr/bin/env python3
"""
ACRRM Training Posts Scraper
Scrapes all training posts from ACRRM website handling pagination
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import List, Dict

def fetch_page(page_num: int, retries: int = 3) -> str:
    """Fetch a page of results with retry logic"""
    url = "https://mycollege.acrrm.org.au/search/find-training-post"

    for attempt in range(retries):
        try:
            # Add headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }

            # Calculate start rank for pagination
            start_rank = (page_num - 1) * 10 + 1

            # Add required parameters for pagination
            params = {
                'query': '',
                'collection': 'acrrm-fatp-public',
                'start_rank': start_rank
            }

            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for page {page_num}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise

    return ""

def parse_training_post(container) -> Dict:
    """Parse a single training post container"""
    data = {}

    try:
        # Site name
        name_elem = container.find('div', class_='srTitle')
        if name_elem:
            data['name'] = name_elem.get_text(strip=True)

        # Parse all the srTpDetails divs
        details_divs = container.find_all('div', class_='srTpDetails')

        for div in details_divs:
            text = div.get_text(strip=True)

            # Post type
            if text.startswith('Post type:'):
                data['type'] = text.replace('Post type:', '').strip()

            # Address
            elif text.startswith('Address:'):
                address_text = text.replace('Address:', '').strip()
                # Parse: 83 Wilmot Street, BURNIE, TAS, 7320
                parts = [p.strip() for p in address_text.split(',')]

                if len(parts) >= 3:
                    # Last part might be postcode
                    if parts[-1].isdigit():
                        data['postcode'] = parts[-1]
                        parts = parts[:-1]

                    # Second to last should be state
                    if len(parts) >= 2:
                        data['state'] = parts[-1]
                        data['city'] = parts[-2]

                    # First part(s) are street address
                    if len(parts) >= 3:
                        data['address'] = ', '.join(parts[:-2])
                    else:
                        data['address'] = parts[0] if parts else ""

            # MMM level
            elif text.startswith('MMM:'):
                mmm_text = text.replace('MMM:', '').strip()
                try:
                    data['mmm'] = int(mmm_text)
                except ValueError:
                    pass

            # Accreditation
            elif text.startswith('Accreditation:'):
                accred_text = text.replace('Accreditation:', '').strip()
                # May have multiple, separated by commas or semicolons
                if accred_text:
                    data['trainingTypes'] = [a.strip() for a in re.split(r'[,;]', accred_text)]

            # Associated/Branch sites
            elif text.startswith('Associated') or text.startswith('Branch'):
                sites_text = re.sub(r'^Associated[/\s]*Branch sites?:', '', text, flags=re.IGNORECASE).strip()
                if sites_text:
                    data['associatedSites'] = [s.strip() for s in sites_text.split(',')]

            # Training organisation
            elif text.startswith('Training organisation:'):
                org = text.replace('Training organisation:', '').strip()
                if 'additionalDetails' in data:
                    data['additionalDetails'] += f" | Organisation: {org}"
                else:
                    data['additionalDetails'] = f"Organisation: {org}"

        # Experience offered (rotations)
        exp_section = container.find('div', class_='srCallOut')
        if exp_section:
            exp_items = exp_section.find_all('li')
            experiences = []
            for li in exp_items:
                text = li.get_text(strip=True)
                # Remove icon text if present
                text = re.sub(r'^(icon-tick|icon-cross)\s+(green|red)\s*', '', text)
                if text and not text.startswith('FACRRM'):  # Skip supervisor info
                    experiences.append(text)

            if experiences:
                data['rotations'] = experiences

        # Supervisor information
        supervisor_items = container.find_all('li')
        for li in supervisor_items:
            text = li.get_text(strip=True)
            if 'FACRRM supervisor' in text or 'supervisor' in text.lower():
                if 'additionalDetails' in data:
                    data['additionalDetails'] += f" | {text}"
                else:
                    data['additionalDetails'] = text

    except Exception as e:
        print(f"Error parsing container: {e}")

    return data

def parse_page(html: str) -> List[Dict]:
    """Parse all training posts from a page"""
    soup = BeautifulSoup(html, 'html.parser')

    # Find all training post containers
    containers = soup.find_all('div', class_='srContainer')

    posts = []
    for container in containers:
        post = parse_training_post(container)
        if post and post.get('name'):  # Only add if we got a name
            posts.append(post)

    return posts

def scrape_all_posts(total_expected: int = 1174, posts_per_page: int = 10) -> List[Dict]:
    """Scrape all training posts from all pages"""
    all_posts = []
    total_pages = (total_expected + posts_per_page - 1) // posts_per_page  # Ceiling division

    print(f"Starting scrape of {total_expected} posts across {total_pages} pages...")

    for page_num in range(1, total_pages + 1):
        try:
            print(f"Fetching page {page_num}/{total_pages}...", end=' ')
            html = fetch_page(page_num)

            posts = parse_page(html)
            print(f"Found {len(posts)} posts")

            if posts:
                all_posts.extend(posts)
            else:
                print(f"  Warning: No posts found on page {page_num}")
                # If we get multiple empty pages in a row, stop
                if page_num > 1 and len(all_posts) < (page_num - 1) * posts_per_page * 0.5:
                    print("  Stopping due to too many empty pages")
                    break

            # Be respectful with rate limiting
            if page_num < total_pages:
                time.sleep(1)  # 1 second between requests

            # Progress update every 10 pages
            if page_num % 10 == 0:
                print(f"Progress: {len(all_posts)} posts collected so far...")

        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            continue

    print(f"\nScraping complete! Collected {len(all_posts)} posts")
    return all_posts

def save_to_json(posts: List[Dict], filename: str):
    """Save posts to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {filename}")

def main():
    """Main execution function"""
    print("ACRRM Training Posts Scraper")
    print("=" * 50)

    # Scrape all posts
    all_posts = scrape_all_posts()

    # Remove duplicates based on name (in case any duplicates slip through)
    seen_names = set()
    unique_posts = []
    for post in all_posts:
        name = post.get('name', '')
        if name and name not in seen_names:
            seen_names.add(name)
            unique_posts.append(post)

    if len(unique_posts) < len(all_posts):
        print(f"Removed {len(all_posts) - len(unique_posts)} duplicate posts")
        all_posts = unique_posts

    # Save to JSON
    output_file = "/Users/fergaltemple/acrrm-all-sites.json"
    save_to_json(all_posts, output_file)

    # Print summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"Total posts collected: {len(all_posts)}")

    if all_posts:
        # Show some statistics
        states = {}
        types = {}
        mmm_levels = {}

        for post in all_posts:
            if 'state' in post:
                states[post['state']] = states.get(post['state'], 0) + 1
            if 'type' in post:
                types[post['type']] = types.get(post['type'], 0) + 1
            if 'mmm' in post:
                mmm = post['mmm']
                mmm_levels[mmm] = mmm_levels.get(mmm, 0) + 1

        print(f"\nBy State:")
        for state, count in sorted(states.items()):
            print(f"  {state}: {count}")

        print(f"\nBy Type:")
        for ptype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ptype}: {count}")

        print(f"\nBy MMM Level:")
        for mmm, count in sorted(mmm_levels.items()):
            print(f"  MMM {mmm}: {count}")

        # Show sample post
        print(f"\nSample post:")
        print(json.dumps(all_posts[0], indent=2))

    print("\nDone!")

if __name__ == "__main__":
    main()
