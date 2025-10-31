#!/usr/bin/env python3
"""
Geocode RANZCOG sites and merge with existing ACRRM data.
"""

import json
import time
import requests
from typing import Dict, Optional
import sys
import os

def geocode_hospital(hospital_name: str) -> Optional[Dict[str, float]]:
    """
    Geocode a hospital name using Nominatim (OpenStreetMap).

    Args:
        hospital_name: Name of the hospital

    Returns:
        Dict with 'lat' and 'lng' keys, or None if geocoding failed
    """
    # Build query string
    query = f"{hospital_name}, Australia"

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

def geocode_ranzcog_sites(input_file: str, output_file: str):
    """
    Add coordinates to RANZCOG sites.

    Args:
        input_file: Path to input JSON file with raw RANZCOG data
        output_file: Path to output JSON file with geocoded data
    """
    # Load sites
    print(f"Loading RANZCOG sites from {input_file}...")
    with open(input_file, 'r') as f:
        sites = json.load(f)

    print(f"Found {len(sites)} RANZCOG sites")
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
        print(f"[{i}/{len(sites)}] Geocoding {site['name']}...")

        coords = geocode_hospital(site['name'])

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

        # Save progress every 50 sites
        if i % 50 == 0:
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

def merge_datasets(acrrm_file: str, ranzcog_file: str, output_file: str):
    """
    Merge ACRRM and RANZCOG datasets, avoiding duplicates.

    Args:
        acrrm_file: Path to ACRRM training sites JSON
        ranzcog_file: Path to geocoded RANZCOG sites JSON
        output_file: Path to output merged JSON
    """
    print(f"\n{'='*60}")
    print("Merging datasets...")

    # Load both datasets
    print(f"Loading ACRRM sites from {acrrm_file}...")
    with open(acrrm_file, 'r') as f:
        acrrm_sites = json.load(f)

    print(f"Loading RANZCOG sites from {ranzcog_file}...")
    with open(ranzcog_file, 'r') as f:
        ranzcog_sites = json.load(f)

    print(f"\nACRRM sites: {len(acrrm_sites)}")
    print(f"RANZCOG sites: {len(ranzcog_sites)}")

    # Create a set of normalized ACRRM hospital names for duplicate detection
    acrrm_names = set()
    for site in acrrm_sites:
        name = site.get('name', '').upper().strip()
        acrrm_names.add(name)

    # Add RANZCOG sites that don't already exist in ACRRM data
    new_sites = 0
    duplicates = 0

    for ranzcog_site in ranzcog_sites:
        name = ranzcog_site.get('name', '').upper().strip()

        # Check for duplicate
        if name in acrrm_names:
            print(f"Skipping duplicate: {ranzcog_site['name']}")
            duplicates += 1
            continue

        # Add unique site
        acrrm_sites.append(ranzcog_site)
        acrrm_names.add(name)
        new_sites += 1

    print(f"\n{'='*60}")
    print(f"Merge complete!")
    print(f"New sites added: {new_sites}")
    print(f"Duplicates skipped: {duplicates}")
    print(f"Total sites in merged dataset: {len(acrrm_sites)}")
    print(f"\nSaving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(acrrm_sites, f, indent=2)

    print("Done!")

if __name__ == "__main__":
    base_path = "/Users/fergaltemple/Documents/Utilities/Software/acrrmTrainingMap"

    # File paths
    ranzcog_raw = f"{base_path}/accrm-scraping/ranzcog-sites-raw.json"
    ranzcog_geocoded = f"{base_path}/accrm-scraping/ranzcog-sites-geocoded.json"
    acrrm_data = f"{base_path}/public/data/training-sites-full.json"
    merged_output = f"{base_path}/public/data/training-sites-full.json"

    print("RANZCOG + ACRRM Data Integration")
    print("=" * 60)
    print("\nStep 1: Geocoding RANZCOG sites")
    print("-" * 60)

    # Geocode RANZCOG sites
    geocoded_sites = geocode_ranzcog_sites(ranzcog_raw, ranzcog_geocoded)

    print("\n\nStep 2: Merging with ACRRM data")
    print("-" * 60)

    # Merge datasets
    merge_datasets(acrrm_data, ranzcog_geocoded, merged_output)

    print("\n" + "=" * 60)
    print("All tasks complete!")
    print("=" * 60)
