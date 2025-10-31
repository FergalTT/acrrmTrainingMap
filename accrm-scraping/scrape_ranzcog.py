#!/usr/bin/env python3
"""
Scrape RANZCOG training sites from https://ranzcog.edu.au/training/sites/
Extracts hospital names and training types (CWH, PTP, APTP) from all state tabs.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re

def scrape_ranzcog_sites():
    """
    Scrape RANZCOG training sites from all state tabs.
    """
    url = "https://ranzcog.edu.au/training/sites/"

    print("Fetching RANZCOG training sites page...")
    print(f"URL: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        print(f"Successfully fetched page (status {response.status_code})")
    except Exception as e:
        print(f"Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Save the HTML for debugging
    with open('ranzcog_page_source.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Saved page source to ranzcog_page_source.html")

    sites = []

    # The page uses tab content for different states
    # Look for state tabs/content sections
    states = ['NSW/ACT', 'QLD', 'SA/NT', 'TAS', 'VIC', 'WA', 'NZ']

    print("\nLooking for training sites data...")

    # Try to find tables or structured content
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables on page")

    for idx, table in enumerate(tables):
        print(f"\nProcessing table {idx + 1}...")

        # Look for header row to identify columns
        headers = []
        header_row = table.find('thead')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
            print(f"Headers: {headers}")

        # Process table rows
        rows = table.find_all('tr')
        print(f"Found {len(rows)} rows")

        for row in rows[1:]:  # Skip header row
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                hospital_name = cells[0].get_text(strip=True)

                if not hospital_name or hospital_name.lower() == 'hospital':
                    continue

                # Extract training types from checkmarks in cells
                training_types = []

                # Check for CWH, PTP, APTP columns
                if len(cells) >= 4:
                    # Assuming columns are: Hospital, CWH, PTP, APTP
                    if '✔' in cells[1].get_text() or '✓' in cells[1].get_text():
                        training_types.append('Core Women\'s Health (CWH)')
                    if '✔' in cells[2].get_text() or '✓' in cells[2].get_text():
                        training_types.append('Practical Training Programme (PTP)')
                    if '✔' in cells[3].get_text() or '✓' in cells[3].get_text():
                        training_types.append('Advanced Practical Training Programme (APTP)')

                site = {
                    'name': hospital_name,
                    'source': 'RANZCOG',
                    'trainingTypes': training_types if training_types else ['O&G Training'],
                    'type': 'Hospital',
                    'sourceUrl': url
                }

                sites.append(site)
                print(f"  Added: {hospital_name} - {', '.join(training_types) if training_types else 'O&G Training'}")

    # Also try to find tab panels/content
    tab_panels = soup.find_all(['div'], class_=re.compile('tab|panel|content', re.I))
    print(f"\nFound {len(tab_panels)} potential tab panels")

    print(f"\n{'='*60}")
    print(f"Total sites scraped: {len(sites)}")

    return sites


def geocode_hospital(hospital_name, state=None):
    """
    Geocode a hospital using Nominatim (OpenStreetMap).
    """
    query = f"{hospital_name}, Australia"
    if state:
        query = f"{hospital_name}, {state}, Australia"

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'au'
    }
    headers = {
        'User-Agent': 'ACRRM-Training-Map/1.0 (Educational Use)'
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json()

        if results and len(results) > 0:
            lat = float(results[0]['lat'])
            lng = float(results[0]['lon'])

            # Extract address components
            display_name = results[0].get('display_name', '')
            address_parts = display_name.split(', ')

            return {
                'lat': lat,
                'lng': lng,
                'city': address_parts[-4] if len(address_parts) >= 4 else '',
                'state': address_parts[-3] if len(address_parts) >= 3 else '',
                'postcode': address_parts[-2] if len(address_parts) >= 2 else ''
            }
        return None
    except Exception as e:
        print(f"  Error geocoding {hospital_name}: {e}")
        return None


if __name__ == "__main__":
    print("RANZCOG Training Sites Scraper")
    print("=" * 60)

    # Scrape sites
    sites = scrape_ranzcog_sites()

    if not sites:
        print("\nNo sites found. Please check the page structure.")
        exit(1)

    # Save raw scraped data
    output_file = 'ranzcog-sites-raw.json'
    with open(output_file, 'w') as f:
        json.dump(sites, f, indent=2)
    print(f"\nSaved raw data to {output_file}")

    # Ask user if they want to geocode
    print("\nWould you like to geocode the addresses now?")
    print("This will take approximately {} seconds (1 second delay between requests)".format(len(sites)))
    response = input("Geocode now? (y/n): ")

    if response.lower() == 'y':
        print("\nGeocoding hospitals...")
        successful = 0
        failed = 0

        for i, site in enumerate(sites, 1):
            print(f"[{i}/{len(sites)}] Geocoding {site['name']}...")

            coords = geocode_hospital(site['name'])

            if coords:
                site['lat'] = coords['lat']
                site['lng'] = coords['lng']
                site['city'] = coords['city']
                site['state'] = coords['state']
                site['postcode'] = coords['postcode']
                print(f"  ✓ Success: {coords['lat']}, {coords['lng']} - {coords['city']}, {coords['state']}")
                successful += 1
            else:
                print(f"  ✗ Failed to geocode")
                failed += 1
                # Set default coordinates for Australian center
                site['lat'] = -25.2744
                site['lng'] = 133.7751
                site['geocoding_failed'] = True

            # Rate limiting - Nominatim allows 1 request per second
            if i < len(sites):
                time.sleep(1.1)

        print(f"\n{'='*60}")
        print(f"Geocoding complete!")
        print(f"Successful: {successful}/{len(sites)} ({successful/len(sites)*100:.1f}%)")
        print(f"Failed: {failed}/{len(sites)} ({failed/len(sites)*100:.1f}%)")

        # Save geocoded data
        geocoded_file = 'ranzcog-sites-geocoded.json'
        with open(geocoded_file, 'w') as f:
            json.dump(sites, f, indent=2)
        print(f"\nSaved geocoded data to {geocoded_file}")

    print("\nDone!")
