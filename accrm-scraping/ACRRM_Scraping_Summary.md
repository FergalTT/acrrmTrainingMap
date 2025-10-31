# ACRRM Training Posts - Scraping Summary

## Overview
Successfully scraped all training posts from the ACRRM (Australian College of Rural and Remote Medicine) website at: https://mycollege.acrrm.org.au/search/find-training-post

## Results

### Data Collection
- **Total pages scraped**: 118 pages
- **Total posts collected**: 1,174 posts
- **Duplicates removed**: 253 duplicates
- **Unique training posts**: 921 unique sites
- **Output file**: `/Users/fergaltemple/acrrm-all-sites.json`
- **File size**: 504 KB

### Data Structure
Each training post includes:
- Site name
- Full address (street, city, state, postcode)
- Post type (General Practice, Hospital, Aboriginal Medical Service, etc.)
- MMM (Modified Monash Model) level (1-7)
- Training/accreditation types
- Experience offered (rotations)
- Associated/branch sites (where applicable)
- Additional details (training organization, supervisor information)

### Key Statistics

#### Geographic Distribution
- **NSW**: 272 posts (29.5%)
- **QLD**: 240 posts (26.1%)
- **VIC**: 126 posts (13.7%)
- **WA**: 93 posts (10.1%)
- **NT**: 70 posts (7.6%)
- **SA**: 68 posts (7.4%)
- **TAS**: 51 posts (5.5%)

#### MMM Level Distribution
- **MMM 5**: 226 posts (24.5%) - Most remote/rural
- **MMM 4**: 193 posts (21.0%)
- **MMM 3**: 192 posts (20.8%)
- **MMM 2**: 147 posts (16.0%)
- **MMM 6**: 65 posts (7.1%)
- **MMM 7**: 57 posts (6.2%)
- **MMM 1**: 39 posts (4.2%) - Major cities

#### Post Type Distribution
- **General Practice**: 548 posts (59.5%)
- **Hospital**: 112 posts (12.2%)
- **Aboriginal Medical Service**: 53 posts (5.8%)
- **Aboriginal Medical Service + GP**: 36 posts (3.9%)
- **General Practice + Hospital**: 26 posts (2.8%)
- **Royal Flying Doctor Service**: 9 posts (1.0%)
- **Australian Defence Force (ADF)**: 4 posts (0.4%)
- **Other combinations**: 6 posts

#### Training Types
- **Core Generalist Training**: 815 posts (88.5%)
- **AST - Emergency Medicine**: 58 posts (6.3%)
- **AST - Palliative Care**: 12 posts (1.3%)
- **AST - Paediatrics**: 8 posts (0.9%)
- **AST - Mental Health**: 7 posts (0.8%)
- **AST - Aboriginal and Torres Strait**: 7 posts (0.8%)
- **Other AST types**: Various specialties

#### Associated Sites
- **Posts with associated sites**: 433 posts (47.0%)

### Data Quality
- **Name**: 100% complete (921/921)
- **State**: 99.9% complete (920/921)
- **City**: 99.9% complete (920/921)
- **Postcode**: 99.9% complete (920/921)
- **Address**: 99.9% complete (920/921)
- **MMM Level**: 99.8% complete (919/921)
- **Training Types**: 100% complete (921/921)
- **Rotations**: 88.5% complete (815/921)
- **Post Type**: 86.2% complete (794/921)

### Top Training Locations
1. Toowoomba (QLD) - 9 posts
2. Broken Hill (NSW) - 8 posts
3. Port Macquarie (NSW) - 8 posts
4. Coffs Harbour (NSW) - 8 posts
5. Tamworth (NSW) - 7 posts
6. Alice Springs (NT) - 7 posts
7. Burnie (TAS) - 6 posts
8. Broome (WA) - 6 posts
9. Mackay (QLD) - 6 posts
10. Bairnsdale (VIC) - 6 posts

## Technical Approach

### Challenge
The website uses pagination with "lazy loading" and a "see more results" button. Initially showing only 10 results per page, with 1,174 total posts across 118 pages.

### Solution
1. Analyzed the HTML structure to identify result containers (`div.srContainer`)
2. Identified the pagination mechanism using URL parameters:
   - `query=` (empty for all results)
   - `collection=acrrm-fatp-public`
   - `start_rank=N` (where N = (page-1) * 10 + 1)
3. Created a Python scraper using:
   - `requests` for HTTP requests
   - `BeautifulSoup` for HTML parsing
   - Rate limiting (1 second between requests)
   - Retry logic for failed requests
   - Duplicate detection and removal
4. Implemented robust parsing to extract all fields from each training post
5. Exported data to structured JSON format

### Scripts Created
- `/Users/fergaltemple/scrape_acrrm.py` - Main scraper script
- `/Users/fergaltemple/analyze_acrrm_data.py` - Data analysis script

## Sample Record
```json
{
  "name": "Bass House Surgery",
  "additionalDetails": "Organisation: The Australian College of Rural and Remote Medicine | FACRRM supervisor(s)",
  "type": "General Practice",
  "postcode": "7320",
  "state": "TAS",
  "city": "BURNIE",
  "address": "83 Wilmot Street",
  "associatedSites": [
    "North West Private Hospital"
  ],
  "mmm": 3,
  "trainingTypes": [
    "Core Generalist Training"
  ],
  "rotations": [
    "Rural and remote context",
    "Primary care",
    "Hospital in patient care",
    "Emergency care"
  ]
}
```

## Notes
- Data collected on: October 15, 2025
- The scraper respects the website with appropriate rate limiting
- Duplicate posts were identified and removed based on site name
- Some posts had multiple training types or post types listed
- 253 duplicates suggest some sites offer multiple training positions or have been listed multiple times
- Data is suitable for training planning and educational purposes

## Files Generated
1. `/Users/fergaltemple/acrrm-all-sites.json` - Complete dataset (921 unique posts)
2. `/Users/fergaltemple/scrape_acrrm.py` - Scraper script
3. `/Users/fergaltemple/analyze_acrrm_data.py` - Analysis script
4. `/Users/fergaltemple/scrape_log.txt` - Scraping log
5. `/Users/fergaltemple/ACRRM_Scraping_Summary.md` - This summary document
