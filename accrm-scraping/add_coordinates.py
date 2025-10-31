#!/usr/bin/env python3
"""
Add coordinates to ACRRM training sites using geocoding.
Uses Nominatim (OpenStreetMap) geocoding service with rate limiting.
"""

import json
import time
import requests
from typing import Dict, Optional, List
import sys

def geocode_address(address: str, city: str, state: str, postcode: str) -> Optional[Dict[str, float]]:
    """
    Geocode an address using Nominatim (OpenStreetMap).

    Args:
        address: Street address
        city: City/suburb name
        state: Australian state code
        postcode: Postcode

    Returns:
        Dict with 'lat' and 'lng' keys, or None if geocoding failed
    """
    # Build query string
    query_parts = []
    if address:
        query_parts.append(address)
    if city:
        query_parts.append(city)
    if state:
        query_parts.append(state)
    if postcode:
        query_parts.append(postcode)
    query_parts.append("Australia")

    query = ", ".join(query_parts)

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
            # Try with just city, state, postcode if full address fails
            if address:
                simpler_query = f"{city}, {state} {postcode}, Australia"
                params['q'] = simpler_query
                response = requests.get(url, params=params, headers=headers, timeout=10)
                results = response.json()
                if results and len(results) > 0:
                    lat = float(results[0]['lat'])
                    lng = float(results[0]['lon'])
                    return {'lat': lat, 'lng': lng}
            return None

    except Exception as e:
        print(f"Error geocoding '{query}': {e}", file=sys.stderr)
        return None

def add_coordinates_to_sites(input_file: str, output_file: str):
    """
    Add coordinates to all sites in the JSON file.

    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
    """
    # Load sites
    print(f"Loading sites from {input_file}...")
    with open(input_file, 'r') as f:
        sites = json.load(f)

    print(f"Found {len(sites)} sites")

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
        print(f"[{i}/{len(sites)}] Geocoding {site['name']} in {site.get('city', 'Unknown')}, {site.get('state', 'Unknown')}...")

        coords = geocode_address(
            site.get('address', ''),
            site.get('city', ''),
            site.get('state', ''),
            site.get('postcode', '')
        )

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
            print(f"\nSaving progress... ({successful} successful, {failed} failed so far)")
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

if __name__ == "__main__":
    input_file = "/Users/fergaltemple/acrrm-all-sites.json"
    output_file = "/Users/fergaltemple/acrrm-all-sites-with-coords.json"

    print("ACRRM Training Sites - Coordinate Geocoding")
    print("=" * 60)
    print("This will add latitude/longitude coordinates to all training sites")
    print("using OpenStreetMap's Nominatim geocoding service.")
    print(f"\nInput:  {input_file}")
    print(f"Output: {output_file}")
    print("\nNote: This will take approximately 15-20 minutes for 921 sites")
    print("      (1 second delay between requests for rate limiting)")
    print("=" * 60)
    print("\nStarting geocoding...")

    add_coordinates_to_sites(input_file, output_file)
