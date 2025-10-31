#!/usr/bin/env python3
"""Analyze the scraped ACRRM training posts data"""

import json
from collections import Counter

# Load the data
with open('/Users/fergaltemple/acrrm-all-sites.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print("=" * 70)
print("ACRRM Training Posts Data Analysis")
print("=" * 70)
print(f"\nTotal unique training posts: {len(posts)}")

# Count posts by state
states = Counter(post.get('state', 'Unknown') for post in posts)
print(f"\n{'State Distribution:':<30}")
print("-" * 70)
for state, count in sorted(states.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(posts)) * 100
    print(f"  {state:<10} {count:>4} posts ({pct:>5.1f}%)")

# Count by MMM level
mmm_levels = Counter(post.get('mmm', 'Unknown') for post in posts)
print(f"\n{'MMM Level Distribution:':<30}")
print("-" * 70)
# Separate numeric and non-numeric MMM values
numeric_mmm = {k: v for k, v in mmm_levels.items() if isinstance(k, int)}
other_mmm = {k: v for k, v in mmm_levels.items() if not isinstance(k, int)}

for mmm, count in sorted(numeric_mmm.items()):
    pct = (count / len(posts)) * 100
    print(f"  MMM {mmm}      {count:>4} posts ({pct:>5.1f}%)")

for mmm, count in other_mmm.items():
    pct = (count / len(posts)) * 100
    print(f"  {mmm:<10} {count:>4} posts ({pct:>5.1f}%)")

# Count by post type
types = Counter(post.get('type', 'Unknown') for post in posts)
print(f"\n{'Post Type Distribution:':<30}")
print("-" * 70)
for ptype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(posts)) * 100
    print(f"  {ptype:<45} {count:>4} posts ({pct:>5.1f}%)")

# Training types
all_training_types = []
for post in posts:
    training_types = post.get('trainingTypes', [])
    all_training_types.extend(training_types)

training_type_counts = Counter(all_training_types)
print(f"\n{'Training/Accreditation Types:':<30}")
print("-" * 70)
for ttype, count in sorted(training_type_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
    pct = (count / len(posts)) * 100
    print(f"  {ttype:<50} {count:>4} ({pct:>5.1f}%)")

# Posts with associated sites
with_associated = sum(1 for post in posts if post.get('associatedSites'))
print(f"\n{'Associated Sites:':<30}")
print("-" * 70)
print(f"  Posts with associated sites: {with_associated} ({(with_associated/len(posts))*100:.1f}%)")

# Experience/Rotations offered
all_rotations = []
for post in posts:
    rotations = post.get('rotations', [])
    all_rotations.extend(rotations)

rotation_counts = Counter(all_rotations)
print(f"\n{'Experience/Rotations Offered:':<30}")
print("-" * 70)
for rotation, count in sorted(rotation_counts.items(), key=lambda x: x[1], reverse=True):
    pct = (count / len(posts)) * 100
    print(f"  {rotation:<50} {count:>4} ({pct:>5.1f}%)")

# Data completeness
print(f"\n{'Data Completeness:':<30}")
print("-" * 70)
fields = ['name', 'state', 'city', 'postcode', 'address', 'type', 'mmm', 'trainingTypes', 'rotations']
for field in fields:
    count = sum(1 for post in posts if post.get(field))
    pct = (count / len(posts)) * 100
    print(f"  {field:<20} {count:>4} / {len(posts)} ({pct:>5.1f}%)")

# Top 10 cities by number of posts
city_counts = Counter(post.get('city', 'Unknown') for post in posts)
print(f"\n{'Top 20 Cities by Training Posts:':<30}")
print("-" * 70)
for city, count in city_counts.most_common(20):
    print(f"  {city:<40} {count:>4} posts")

print("\n" + "=" * 70)
print("Analysis complete!")
print("=" * 70)
