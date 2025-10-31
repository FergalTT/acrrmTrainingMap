#!/usr/bin/env python3
"""
Geocode ANZCA sites and merge with existing ACRRM data.
"""

import json
import time
import requests
from typing import Dict, Optional
import sys

def geocode_hospital(hospital_name: str, state: str) -> Optional[Dict[str, float]]:
    """
    Geocode a hospital name using Nominatim (OpenStreetMap).

    Args:
        hospital_name: Name of the hospital
        state: Australian state code

    Returns:
        Dict with 'lat' and 'lng' keys, or None if geocoding failed
    """
    # Build query string - include state for better accuracy
    query = f"{hospital_name}, {state}, Australia"

    # Nominatim API endpoint
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
            return {'lat': lat, 'lng': lng}
        else:
            return None

    except Exception as e:
        print(f"Error geocoding '{hospital_name}': {e}", file=sys.stderr)
        return None

def geocode_anzca_sites(input_file: str, output_file: str):
    """
    Add coordinates to ANZCA sites.

    Args:
        input_file: Path to input JSON file with raw ANZCA data
        output_file: Path to output JSON file with geocoded data
    """
    # Load sites
    print(f"Loading ANZCA sites from {input_file}...")
    with open(input_file, 'r') as f:
        sites = json.load(f)

    print(f"Found {len(sites)} ANZCA sites")
    print("Starting geocoding...\n")

    # Process each site
    successful = 0
    failed = 0

    for i, site in enumerate(sites, 1):
        # Check if coordinates already exist
        if 'lat' in site and 'lng' in site:
            print(f"[{i}/{len(sites)}] {site['name']} - Already has coordinates")
            successful += 1
            continue

        # Geocode
        state = site.get('state', '')
        print(f"[{i}/{len(sites)}] Geocoding {site['name']} ({state})...")

        coords = geocode_hospital(site['name'], state)

        if coords:
            site['lat'] = coords['lat']
            site['lng'] = coords['lng']
            print(f"  ✓ Success: {coords['lat']}, {coords['lng']}")
            successful += 1
        else:
            print(f"  ✗ Failed to geocode")
            failed += 1
            # Set default coordinates for Australian center so site still appears
            site['lat'] = -25.2744
            site['lng'] = 133.7751
            site['geocoding_failed'] = True

        # Rate limiting - Nominatim allows 1 request per second
        if i < len(sites):  # Don't sleep after last item
            time.sleep(1.1)  # Slightly over 1 second to be safe

        # Save progress every 20 sites
        if i % 20 == 0:
            print(f"\nSaving progress... ({successful} successful, {failed} failed so far)\n")
            with open(output_file, 'w') as f:
                json.dump(sites, f, indent=2)

    # Save final results
    print(f"\n{'='*60}")
    print(f"Geocoding complete!")
    print(f"Successful: {successful}/{len(sites)} ({successful/len(sites)*100:.1f}%)")
    print(f"Failed: {failed}/{len(sites)} ({failed/len(sites)*100:.1f}%)")
    print(f"\nSaving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(sites, f, indent=2)

    print("Done!")
    return sites

def merge_datasets(acrrm_file: str, anzca_file: str, output_file: str):
    """
    Merge ACRRM and ANZCA datasets, avoiding duplicates.

    Args:
        acrrm_file: Path to existing training sites JSON (with ACRRM + RANZCOG)
        anzca_file: Path to geocoded ANZCA sites JSON
        output_file: Path to output merged JSON
    """
    print(f"\n{'='*60}")
    print("Merging datasets...")

    # Load both datasets
    print(f"Loading existing sites from {acrrm_file}...")
    with open(acrrm_file, 'r') as f:
        existing_sites = json.load(f)

    print(f"Loading ANZCA sites from {anzca_file}...")
    with open(anzca_file, 'r') as f:
        anzca_sites = json.load(f)

    print(f"\nExisting sites: {len(existing_sites)}")
    print(f"ANZCA sites: {len(anzca_sites)}")

    # Create a set of normalized hospital names for duplicate detection
    existing_names = set()
    for site in existing_sites:
        name = site.get('name', '').upper().strip()
        existing_names.add(name)

    # Add ANZCA sites that don't already exist
    new_sites = 0
    duplicates = 0

    for anzca_site in anzca_sites:
        name = anzca_site.get('name', '').upper().strip()

        # Check for duplicate
        if name in existing_names:
            print(f"Skipping duplicate: {anzca_site['name']}")
            duplicates += 1
            continue

        # Add unique site
        existing_sites.append(anzca_site)
        existing_names.add(name)
        new_sites += 1

    print(f"\n{'='*60}")
    print(f"Merge complete!")
    print(f"New sites added: {new_sites}")
    print(f"Duplicates skipped: {duplicates}")
    print(f"Total sites in merged dataset: {len(existing_sites)}")
    print(f"\nSaving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(existing_sites, f, indent=2)

    print("Done!")

if __name__ == "__main__":
    base_path = "/Users/fergaltemple/Documents/Utilities/Software/acrrmTrainingMap"

    # File paths
    anzca_raw = f"{base_path}/accrm-scraping/anzca-sites-raw.json"
    anzca_geocoded = f"{base_path}/accrm-scraping/anzca-sites-geocoded.json"
    existing_data = f"{base_path}/public/data/training-sites-full.json"
    merged_output = f"{base_path}/public/data/training-sites-full.json"

    print("ANZCA + ACRRM Data Integration")
    print("=" * 60)
    print("\nStep 1: Geocoding ANZCA sites")
    print("-" * 60)

    # Geocode ANZCA sites
    geocoded_sites = geocode_anzca_sites(anzca_raw, anzca_geocoded)

    print("\n\nStep 2: Merging with existing data")
    print("-" * 60)

    # Merge datasets
    merge_datasets(existing_data, anzca_geocoded, merged_output)

    print("\n" + "=" * 60)
    print("All tasks complete!")
    print("=" * 60)
