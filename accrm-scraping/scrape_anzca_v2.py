#!/usr/bin/env python3
"""
Scrape ANZCA Rural Generalist Anaesthesia training sites from state pages.
Uses requests + BeautifulSoup to extract hospital names and cities.
"""

import json
import time
import requests
from bs4 import BeautifulSoup
import re
import sys

def scrape_state_page(state_code, state_name, url):
    """
    Scrape training sites for a specific state.

    Args:
        state_code: State abbreviation (NSW, VIC, etc.)
        state_name: Full state name
        url: Full URL to the state's training sites page

    Returns:
        List of training sites
    """
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

        # Save HTML for debugging
        debug_file = f"/Users/fergaltemple/Documents/Utilities/Software/acrrmTrainingMap/accrm-scraping/anzca_{state_code.lower()}_page.html"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"  Saved HTML to: {debug_file}")

        # Look for hospital names in <p> tags
        # Find all paragraphs that contain hospital keywords
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            text = p.get_text().strip()

            # Look for hospital keywords
            if any(keyword in text.lower() for keyword in [
                'hospital', 'health campus', 'health service', 'medical centre', 'medical center'
            ]):
                # Skip very long paragraphs (descriptions, not names)
                if len(text) < 150 and len(text) > 5:
                    # Skip paragraphs that are clearly not hospital names
                    if not any(skip in text.lower() for skip in [
                        'find an', 'training site', 'director of', 'supervisor',
                        'email', '@', 'http', 'phone', 'contact', 'accredited',
                        'must be', 'should', 'will', 'can be', 'training time'
                    ]):
                        # Clean up the hospital name
                        hospital_name = text.strip()

                        # Remove HTML entities and extra whitespace
                        hospital_name = re.sub(r'\s+', ' ', hospital_name)
                        hospital_name = re.sub(r'&nbsp;', ' ', hospital_name)

                        # Skip standalone words like "Hospital"
                        if hospital_name.lower().strip() == 'hospital':
                            continue

                        # Check if already in list
                        if hospital_name and hospital_name not in [s['name'] for s in sites]:
                            # Try to extract city name (often in parentheses)
                            city = None

                            # Look for parentheses with potential city/abbreviation
                            paren_match = re.search(r'\(([^)]+)\)', hospital_name)
                            if paren_match:
                                potential_city = paren_match.group(1)
                                # If it's likely an abbreviation, keep it in the name
                                if len(potential_city) > 10:  # Likely a full description, not abbreviation
                                    city = potential_city
                                    hospital_name = re.sub(r'\s*\([^)]+\)', '', hospital_name).strip()

                            site = {
                                'name': hospital_name,
                                'source': 'ANZCA',
                                'trainingTypes': ['AST - Anaesthetics'],
                                'type': 'Hospital',
                                'state': state_code,
                                'sourceUrl': url
                            }

                            if city:
                                site['city'] = city

                            sites.append(site)
                            print(f"  Found: {hospital_name}" + (f" ({city})" if city else ""))

        print(f"  Total sites found: {len(sites)}")
        return sites

    except Exception as e:
        print(f"  Error scraping {state_name}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return []

def scrape_all_states():
    """
    Scrape all ANZCA training sites from all state pages.
    """
    base_url = "https://www.anzca.edu.au/education-and-training/anaesthesia-training-and-pathways/rural-generalist-anaesthesia-training-program/rural-generalist-anaesthesia-training-sites"

    states = [
        ('QLD', 'Queensland', f'{base_url}/rga-accredited-training-sites-qld'),
        ('NSW', 'New South Wales', f'{base_url}/rga-anaesthesia-training-sites-act'),  # Also includes ACT
        ('VIC', 'Victoria', f'{base_url}/rga-accredited-training-sites-vic'),
        ('SA', 'South Australia', f'{base_url}/rga-accredited-training-sites-sa'),
        ('WA', 'Western Australia', f'{base_url}/rga-accredited-training-sites-nsw'),  # WA page has wrong URL
        ('TAS', 'Tasmania', f'{base_url}/rga-accredited-training-sites-tas'),
        ('NT', 'Northern Territory', f'{base_url}/rga-accredited-training-sites-nt'),
    ]

    all_sites = []

    print("ANZCA Rural Generalist Anaesthesia Training Sites Scraper v2")
    print("=" * 70)

    for state_code, state_name, url in states:
        sites = scrape_state_page(state_code, state_name, url)
        all_sites.extend(sites)

        # Be polite to the server
        time.sleep(3)

    print(f"\n{'=' * 70}")
    print(f"Total sites scraped: {len(all_sites)}")

    # Save results
    output_file = "/Users/fergaltemple/Documents/Utilities/Software/acrrmTrainingMap/accrm-scraping/anzca-sites-raw.json"
    print(f"Saving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(all_sites, f, indent=2)

    print("Done!")

    # Show breakdown by state
    print("\nSites by state:")
    for state_code, state_name, _ in states:
        count = sum(1 for s in all_sites if s.get('state') == state_code)
        print(f"  {state_code}: {count}")

    return all_sites

if __name__ == "__main__":
    scrape_all_states()
