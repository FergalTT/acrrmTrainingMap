#!/usr/bin/env python3
"""
Scrape ANZCA Rural Generalist Anaesthesia training sites.
"""

import json
import time
import requests
from bs4 import BeautifulSoup
import sys

def scrape_anzca_state_page(state_code: str, state_name: str) -> list:
    """
    Scrape training sites for a specific state.

    Args:
        state_code: State abbreviation (NSW, VIC, etc.)
        state_name: Full state name

    Returns:
        List of training sites
    """
    base_url = "https://www.anzca.edu.au/education-and-training/anaesthesia-training-and-pathways/rural-generalist-anaesthesia-training-program/rural-generalist-anaesthesia-training-sites"
    url = f"{base_url}/rga-accredited-training-sites-{state_code.lower()}"

    print(f"\nScraping {state_name} ({state_code})...")
    print(f"URL: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        sites = []

        # Try to find tables or lists containing hospital information
        # Look for common patterns in hospital names
        content_div = soup.find('div', class_='content') or soup.find('div', id='content') or soup.find('main')

        if content_div:
            # Look for hospital names in various elements
            # Try headings first
            headings = content_div.find_all(['h2', 'h3', 'h4', 'strong'])

            for heading in headings:
                text = heading.get_text().strip()

                # Filter for likely hospital names
                if any(keyword in text.lower() for keyword in [
                    'hospital', 'health', 'medical centre', 'medical center',
                    'clinic', 'campus', 'service'
                ]):
                    # Remove common prefixes/suffixes
                    hospital_name = text.strip()

                    # Skip if it's a section header
                    if len(hospital_name) > 5 and not hospital_name.lower().startswith('satellite'):
                        site = {
                            'name': hospital_name,
                            'source': 'ANZCA',
                            'trainingTypes': ['AST - Anaesthetics'],
                            'type': 'Hospital',
                            'state': state_code,
                            'sourceUrl': url
                        }
                        sites.append(site)
                        print(f"  Found: {hospital_name}")

            # Also look in tables
            tables = content_div.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    for cell in cells:
                        text = cell.get_text().strip()
                        if any(keyword in text.lower() for keyword in [
                            'hospital', 'health campus', 'medical centre'
                        ]) and len(text) < 100:  # Avoid long paragraphs
                            # Clean up the text
                            hospital_name = text.strip()
                            if hospital_name and hospital_name not in [s['name'] for s in sites]:
                                site = {
                                    'name': hospital_name,
                                    'source': 'ANZCA',
                                    'trainingTypes': ['AST - Anaesthetics'],
                                    'type': 'Hospital',
                                    'state': state_code,
                                    'sourceUrl': url
                                }
                                sites.append(site)
                                print(f"  Found: {hospital_name}")

        print(f"  Total sites found: {len(sites)}")
        return sites

    except Exception as e:
        print(f"  Error scraping {state_name}: {e}", file=sys.stderr)
        return []

def scrape_all_anzca_sites(output_file: str):
    """
    Scrape all ANZCA training sites from all states.

    Args:
        output_file: Path to output JSON file
    """
    states = [
        ('NSW', 'New South Wales'),
        ('VIC', 'Victoria'),
        ('QLD', 'Queensland'),
        ('SA', 'South Australia'),
        ('WA', 'Western Australia'),
        ('TAS', 'Tasmania'),
        ('NT', 'Northern Territory'),
    ]

    all_sites = []

    print("ANZCA Rural Generalist Anaesthesia Training Sites Scraper")
    print("=" * 60)

    for state_code, state_name in states:
        sites = scrape_anzca_state_page(state_code, state_name)
        all_sites.extend(sites)

        # Be polite to the server
        time.sleep(2)

    print(f"\n{'=' * 60}")
    print(f"Total sites scraped: {len(all_sites)}")
    print(f"Saving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(all_sites, f, indent=2)

    print("Done!")

    # Show breakdown by state
    print("\nSites by state:")
    for state_code, _ in states:
        count = sum(1 for s in all_sites if s.get('state') == state_code)
        print(f"  {state_code}: {count}")

if __name__ == "__main__":
    base_path = "/Users/fergaltemple/Documents/Utilities/Software/acrrmTrainingMap"
    output_file = f"{base_path}/accrm-scraping/anzca-sites-raw.json"

    scrape_all_anzca_sites(output_file)
