# IPO Fetcher - Summary

## What was Created

I've built a complete Python function to fetch IPO (Initial Public Offer) data from Chittorgarh.com and return it in JSON format, filtered by month and year.

## Files Created

### 1. **ipo_fetcher.py** (Main Module)
The core module containing:
- `fetch_ipo_data(month, year, use_selenium=True)` - Main function to fetch IPO data
- `get_ipo_data_json(month, year)` - Convenience function returning JSON string
- `_fetch_with_selenium()` - Internal function using Selenium for JavaScript rendering
- `_fetch_with_requests()` - Internal function using requests library
- `_parse_date()` - Helper function for date parsing

### 2. **example_usage.py**
Comprehensive examples demonstrating:
- Fetching data for specific months
- Getting data as JSON strings
- Looping through multiple months
- Saving to JSON files
- Filtering IPOs by criteria
- Error handling

### 3. **IPO_FETCHER_README.md**
Complete documentation including:
- Installation instructions
- Usage examples
- API reference
- Data field explanations
- Troubleshooting guide

## Key Features

✅ **Input**: Month (1-12) and Year (e.g., 2025)

✅ **Output**: JSON format with:
- `year`, `month`, `month_name`
- `total_ipos` - count of IPOs in that month
- `ipos` - array of IPO details

✅ **Data per IPO**:
- Company name
- Open date (YYYY-MM-DD)
- Close date (YYYY-MM-DD)
- List date (YYYY-MM-DD or "Yet to list")
- Price (fixed or range)
- Total issue amount in Crores
- Exchange (BSE, NSE, etc.)
- Lead manager/underwriter

✅ **Smart Features**:
- Automatic date parsing from website format
- Month filtering based on close date
- Selenium support for JavaScript-rendered content
- Fallback to requests library
- Comprehensive error handling
- Input validation (month 1-12, year validation)

## Usage Example

```python
from ipo_fetcher import fetch_ipo_data
import json

# Fetch December 2025 IPO data
data = fetch_ipo_data(month=12, year=2025)

# Print as formatted JSON
print(json.dumps(data, indent=2))
```

## Sample Output

```json
{
  "year": 2025,
  "month": 12,
  "month_name": "December",
  "total_ipos": 10,
  "ipos": [
    {
      "company_name": "Gujarat Kidney & Super Speciality Ltd. IPO",
      "open_date": "2025-12-22",
      "close_date": "2025-12-24",
      "list_date": "Yet to list",
      "price": "108.00 to 114.00",
      "total_issue_amount": "250.80",
      "exchange": "BSE, NSE",
      "lead_manager": "Nirbhay Capital"
    },
    ...
  ]
}
```

## Tested Scenarios

✅ December 2025: 10 IPOs
✅ November 2025: 11 IPOs  
✅ October 2025: 4 IPOs
✅ Error handling with invalid input
✅ JSON serialization
✅ Date parsing and filtering

## How to Use

1. Import the function:
```python
from ipo_fetcher import fetch_ipo_data, get_ipo_data_json
```

2. Fetch data:
```python
data = fetch_ipo_data(month=12, year=2025)
```

3. Work with the data:
```python
import json
print(json.dumps(data, indent=2))

# Or access specific fields
for ipo in data['ipos']:
    print(f"{ipo['company_name']}: {ipo['price']}")
```

## Error Handling

The function gracefully handles errors and returns a response with an 'error' field:

```python
data = fetch_ipo_data(month=12, year=2025)
if 'error' in data:
    print(f"Error: {data['error']}")
else:
    print(f"Success: {data['total_ipos']} IPOs found")
```

## Next Steps

You can now:
- Integrate this into your Jupyter notebooks (chittor.ipynb, ipo_checker.ipynb)
- Schedule regular updates to track IPOs
- Build analytics/dashboards on top of this data
- Compare with your ipo_data.csv and ipo_data.json files
- Export to database for analysis

## Requirements

Make sure you have installed:
- `requests`
- `beautifulsoup4` 
- `selenium`

All are already in your requirements.txt and installed in your virtual environment.
