#!/usr/bin/env python3
"""
Update O&G training type labels to merge them into a single 'AST - O&G' category.
"""

import json

def update_training_types(input_file: str, output_file: str):
    """
    Update O&G training type labels to 'AST - O&G'.

    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
    """
    # O&G training types to merge
    og_types = {
        'Advanced Practical Training Programme (APTP)',
        "Core Women's Health (CWH)",
        'O&G Training',
        'Practical Training Programme (PTP)'
    }

    print(f"Loading sites from {input_file}...")
    with open(input_file, 'r') as f:
        sites = json.load(f)

    print(f"Found {len(sites)} sites")

    # Count sites affected
    sites_updated = 0

    for site in sites:
        if 'trainingTypes' in site and site['trainingTypes']:
            # Check if any O&G types are present
            has_og = any(t in og_types for t in site['trainingTypes'])

            if has_og:
                # Remove all O&G types and add single 'AST - O&G' label
                site['trainingTypes'] = [
                    t for t in site['trainingTypes'] if t not in og_types
                ]

                # Add AST - O&G if not already there
                if 'AST - O&G' not in site['trainingTypes']:
                    site['trainingTypes'].append('AST - O&G')

                sites_updated += 1

    print(f"\nUpdated {sites_updated} sites")
    print(f"Saving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(sites, f, indent=2)

    print("Done!")

    # Show updated training types
    all_types = set()
    for site in sites:
        if 'trainingTypes' in site:
            all_types.update(site['trainingTypes'])

    print(f"\nAll training types in dataset:")
    for t in sorted(all_types):
        print(f"  - {t}")

if __name__ == "__main__":
    base_path = "/Users/fergaltemple/Documents/Utilities/Software/acrrmTrainingMap"

    input_file = f"{base_path}/public/data/training-sites-full.json"
    output_file = f"{base_path}/public/data/training-sites-full.json"

    update_training_types(input_file, output_file)
