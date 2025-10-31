#!/usr/bin/env python3
"""
Fast coordinate addition using Australian city/town coordinate database.
This avoids individual geocoding for every site by using known coordinates.
"""

import json

# Australian cities/towns coordinate database
# Coordinates for common training locations
AUSTRALIAN_LOCATIONS = {
    # Queensland
    ("BRISBANE", "QLD"): (-27.4698, 153.0251),
    ("GOLD COAST", "QLD"): (-28.0167, 153.4000),
    ("SUNSHINE COAST", "QLD"): (-26.6500, 153.0667),
    ("TOOWOOMBA", "QLD"): (-27.5598, 151.9507),
    ("CAIRNS", "QLD"): (-16.9203, 145.7710),
    ("TOWNSVILLE", "QLD"): (-19.2590, 146.8169),
    ("MACKAY", "QLD"): (-21.1458, 149.1869),
    ("ROCKHAMPTON", "QLD"): (-23.3781, 150.5136),
    ("BUNDABERG", "QLD"): (-24.8661, 152.3489),
    ("HERVEY BAY", "QLD"): (-25.2887, 152.8275),
    ("MARYBOROUGH", "QLD"): (-25.5384, 152.7013),
    ("GLADSTONE", "QLD"): (-23.8479, 151.2569),
    ("MOUNT ISA", "QLD"): (-20.7256, 139.4927),
    ("IPSWICH", "QLD"): (-27.6144, 152.7575),
    ("LOGAN", "QLD"): (-27.6650, 153.0833),
    ("REDLAND", "QLD"): (-27.5275, 153.2625),
    ("CABOOLTURE", "QLD"): (-27.0833, 152.9500),
    ("KINGAROY", "QLD"): (-26.5400, 151.8367),
    ("MANOORA", "QLD"): (-16.9386, 145.7453),
    ("ENOGGERA", "QLD"): (-27.4253, 152.9908),
    ("CHERMSIDE", "QLD"): (-27.3858, 153.0333),
    ("SOUTHPORT", "QLD"): (-27.9667, 153.4000),
    ("NAMBOUR", "QLD"): (-26.6269, 152.9594),
    ("ROMA", "QLD"): (-26.5714, 148.7867),
    ("EMERALD", "QLD"): (-23.5253, 148.1614),
    ("LONGREACH", "QLD"): (-23.4406, 144.2497),
    ("CHARLEVILLE", "QLD"): (-26.4075, 146.2417),

    # New South Wales
    ("SYDNEY", "NSW"): (-33.8688, 151.2093),
    ("NEWCASTLE", "NSW"): (-32.9283, 151.7817),
    ("WOLLONGONG", "NSW"): (-34.4278, 150.8931),
    ("CENTRAL COAST", "NSW"): (-33.4307, 151.3428),
    ("PENRITH", "NSW"): (-33.7511, 150.6942),
    ("DUBBO", "NSW"): (-32.2569, 148.6011),
    ("WAGGA WAGGA", "NSW"): (-35.1082, 147.3598),
    ("ALBURY", "NSW"): (-36.0737, 146.9135),
    ("TAMWORTH", "NSW"): (-31.0927, 150.9279),
    ("ORANGE", "NSW"): (-33.2831, 149.0989),
    ("BATHURST", "NSW"): (-33.4197, 149.5775),
    ("LISMORE", "NSW"): (-28.8142, 153.2789),
    ("BROKEN HILL", "NSW"): (-31.9559, 141.4583),
    ("COFFS HARBOUR", "NSW"): (-30.2986, 153.1094),
    ("PORT MACQUARIE", "NSW"): (-31.4333, 152.9000),
    ("ARMIDALE", "NSW"): (-30.5128, 151.6644),
    ("MOREE", "NSW"): (-29.4647, 149.8406),
    ("GRIFFITH", "NSW"): (-34.2869, 146.0503),
    ("GOULBURN", "NSW"): (-34.7537, 149.7200),
    ("QUEANBEYAN", "NSW"): (-35.3539, 149.2322),
    ("BOWRAL", "NSW"): (-34.4781, 150.4178),
    ("MUDGEE", "NSW"): (-32.5972, 149.5875),
    ("PARKES", "NSW"): (-33.1361, 148.1744),

    # Victoria
    ("MELBOURNE", "VIC"): (-37.8136, 144.9631),
    ("GEELONG", "VIC"): (-38.1499, 144.3617),
    ("BALLARAT", "VIC"): (-37.5622, 143.8503),
    ("BENDIGO", "VIC"): (-36.7570, 144.2794),
    ("SHEPPARTON", "VIC"): (-36.3806, 145.3989),
    ("WODONGA", "VIC"): (-36.1217, 146.8881),
    ("MILDURA", "VIC"): (-34.1850, 142.1561),
    ("WARRNAMBOOL", "VIC"): (-38.3831, 142.4853),
    ("TRARALGON", "VIC"): (-38.1964, 146.5406),
    ("HORSHAM", "VIC"): (-36.7147, 142.1989),
    ("ECHUCA", "VIC"): (-36.1392, 144.7508),
    ("SALE", "VIC"): (-38.1094, 147.0683),
    ("WANGARATTA", "VIC"): (-36.3581, 146.3178),
    ("SWAN HILL", "VIC"): (-35.3378, 143.5542),
    ("COLAC", "VIC"): (-38.3403, 143.5847),

    # South Australia
    ("ADELAIDE", "SA"): (-34.9285, 138.6007),
    ("MOUNT GAMBIER", "SA"): (-37.8297, 140.7822),
    ("WHYALLA", "SA"): (-33.0339, 137.5264),
    ("PORT AUGUSTA", "SA"): (-32.4928, 137.7656),
    ("PORT LINCOLN", "SA"): (-34.7258, 135.8586),
    ("PORT PIRIE", "SA"): (-33.1856, 138.0169),
    ("MURRAY BRIDGE", "SA"): (-35.1197, 139.2744),
    ("BEDFORD PARK", "SA"): (-35.0017, 138.5683),
    ("ELIZABETH VALE", "SA"): (-34.7617, 138.6881),
    ("WOODVILLE", "SA"): (-34.8686, 138.5389),
    ("VICTOR HARBOR", "SA"): (-35.5518, 138.6178),
    ("GAWLER", "SA"): (-34.5978, 138.7411),

    # Western Australia
    ("PERTH", "WA"): (-31.9505, 115.8605),
    ("FREMANTLE", "WA"): (-32.0569, 115.7439),
    ("BUNBURY", "WA"): (-33.3267, 115.6372),
    ("GERALDTON", "WA"): (-28.7744, 114.6144),
    ("KALGOORLIE", "WA"): (-30.7489, 121.4658),
    ("ALBANY", "WA"): (-35.0239, 117.8844),
    ("BROOME", "WA"): (-17.9556, 122.2392),
    ("PORT HEDLAND", "WA"): (-20.3106, 118.6069),
    ("MANDURAH", "WA"): (-32.5269, 115.7217),
    ("JOONDALUP", "WA"): (-31.7456, 115.7661),
    ("MURDOCH", "WA"): (-32.0444, 115.8356),
    ("BUSSELTON", "WA"): (-33.6500, 115.3500),
    ("CARNARVON", "WA"): (-24.8819, 113.6633),
    ("KARRATHA", "WA"): (-20.7367, 116.8461),

    # Tasmania
    ("HOBART", "TAS"): (-42.8806, 147.3250),
    ("LAUNCESTON", "TAS"): (-41.4419, 147.1361),
    ("BURNIE", "TAS"): (-41.0522, 145.9147),
    ("DEVONPORT", "TAS"): (-41.1761, 146.3494),
    ("KINGSTON", "TAS"): (-42.9803, 147.3081),
    ("ULVERSTONE", "TAS"): (-41.1575, 146.1700),
    ("QUEENSTOWN", "TAS"): (-42.0833, 145.5500),

    # Northern Territory
    ("DARWIN", "NT"): (-12.4634, 130.8456),
    ("ALICE SPRINGS", "NT"): (-23.6980, 133.8807),
    ("KATHERINE", "NT"): (-14.4653, 132.2644),
    ("PALMERSTON", "NT"): (-12.4897, 130.9800),
    ("NHULUNBUY", "NT"): (-12.1992, 136.7731),
    ("YIRRKALA", "NT"): (-12.2514, 136.8881),
    ("TENNANT CREEK", "NT"): (-19.6497, 134.1886),

    # ACT
    ("CANBERRA", "ACT"): (-35.2809, 149.1300),
    ("BELCONNEN", "ACT"): (-35.2386, 149.0650),
    ("WODEN", "ACT"): (-35.3444, 149.0886),
}

def get_coordinates(city: str, state: str) -> tuple:
    """
    Get coordinates for a city/state combination.
    Returns (lat, lng) tuple.
    """
    # Normalize city name
    city_upper = city.upper().strip()
    state_upper = state.upper().strip()

    # Try exact match
    key = (city_upper, state_upper)
    if key in AUSTRALIAN_LOCATIONS:
        return AUSTRALIAN_LOCATIONS[key]

    # Try partial match for suburbs within cities
    for (loc_city, loc_state), coords in AUSTRALIAN_LOCATIONS.items():
        if loc_state == state_upper and loc_city in city_upper:
            return coords

    # Default to state capital if no match
    state_capitals = {
        "QLD": (-27.4698, 153.0251),  # Brisbane
        "NSW": (-33.8688, 151.2093),  # Sydney
        "VIC": (-37.8136, 144.9631),  # Melbourne
        "SA": (-34.9285, 138.6007),   # Adelaide
        "WA": (-31.9505, 115.8605),   # Perth
        "TAS": (-42.8806, 147.3250),  # Hobart
        "NT": (-12.4634, 130.8456),   # Darwin
        "ACT": (-35.2809, 149.1300),  # Canberra
    }

    return state_capitals.get(state_upper, (-25.2744, 133.7751))  # Default to center of Australia

def add_coordinates_fast(input_file: str, output_file: str):
    """
    Quickly add coordinates to all sites using pre-defined city coordinates.
    """
    # Load sites
    print(f"Loading sites from {input_file}...")
    with open(input_file, 'r') as f:
        sites = json.load(f)

    print(f"Found {len(sites)} sites")
    print("Adding coordinates...")

    # Add coordinates to each site
    exact_matches = 0
    fallback_matches = 0

    for i, site in enumerate(sites, 1):
        if 'lat' in site and 'lng' in site:
            print(f"[{i}/{len(sites)}] {site['name']} - Already has coordinates")
            exact_matches += 1
            continue

        city = site.get('city', '')
        state = site.get('state', '')

        # Get coordinates
        lat, lng = get_coordinates(city, state)
        site['lat'] = lat
        site['lng'] = lng

        # Check if exact match or fallback
        key = (city.upper().strip(), state.upper().strip())
        if key in AUSTRALIAN_LOCATIONS:
            exact_matches += 1
            print(f"[{i}/{len(sites)}] ✓ {site['name']} ({city}, {state}) - Exact match")
        else:
            fallback_matches += 1
            print(f"[{i}/{len(sites)}] ~ {site['name']} ({city}, {state}) - Fallback to {state} capital")

    # Save results
    print(f"\n{'='*60}")
    print(f"Coordinate addition complete!")
    print(f"Exact matches: {exact_matches}/{len(sites)} ({exact_matches/len(sites)*100:.1f}%)")
    print(f"Fallback (state capital): {fallback_matches}/{len(sites)} ({fallback_matches/len(sites)*100:.1f}%)")
    print(f"\nSaving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(sites, f, indent=2)

    print("Done!")
    print(f"\nNote: Sites with fallback coordinates will appear at their state capital.")
    print(f"You can manually adjust coordinates later or run full geocoding for exact locations.")

if __name__ == "__main__":
    input_file = "/Users/fergaltemple/acrrm-all-sites.json"
    output_file = "/Users/fergaltemple/acrrm-all-sites-with-coords.json"

    print("ACRRM Training Sites - Fast Coordinate Addition")
    print("=" * 60)

    add_coordinates_fast(input_file, output_file)
