# IPO Fetcher - Chittorgarh.com IPO Data Scraper

A Python utility to fetch Indian IPO (Initial Public Offer) details from Chittorgarh.com and return the data in JSON format.

## Features

- ✅ Fetch IPO data filtered by month and year
- ✅ Returns data in clean JSON format
- ✅ Supports both Selenium (for JavaScript-rendered content) and requests-based fetching
- ✅ Comprehensive error handling
- ✅ Company name, open/close dates, listing date, price, issue amount, exchange, and lead manager
- ✅ Automatic date parsing and month filtering

## Installation

### Prerequisites
- Python 3.7+
- Required packages:
  - `requests`
  - `beautifulsoup4`
  - `selenium`

### Setup

```bash
# Install required packages
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests beautifulsoup4 selenium
```

## Usage

### Basic Usage

```python
from ipo_fetcher import fetch_ipo_data
import json

# Fetch December 2025 IPO data
data = fetch_ipo_data(month=12, year=2025)

# Print as JSON
print(json.dumps(data, indent=2))
```

### Function Signature

```python
def fetch_ipo_data(month: int, year: int, use_selenium: bool = True) -> Dict[str, Any]:
    """
    Fetch IPO details for a specific month and year from Chittorgarh website.
    
    Args:
        month (int): Month number (1-12)
        year (int): Year (e.g., 2025)
        use_selenium (bool): Whether to use Selenium for JavaScript rendering (default: True)
    
    Returns:
        Dict containing IPO data in JSON format
    """
```

### Return Format

```json
{
  "year": 2025,
  "month": 12,
  "month_name": "December",
  "total_ipos": 10,
  "ipos": [
    {
      "company_name": "Company Name Ltd. IPO",
      "open_date": "2025-12-22",
      "close_date": "2025-12-24",
      "list_date": "2025-12-25",
      "price": "100.00 to 110.00",
      "total_issue_amount": "500.50",
      "exchange": "BSE, NSE",
      "lead_manager": "Lead Manager Name"
    }
  ]
}
```

### Examples

#### Example 1: Fetch data for a specific month

```python
from ipo_fetcher import fetch_ipo_data
import json

# Get November 2025 IPOs
data = fetch_ipo_data(month=11, year=2025)
print(f"Total IPOs: {data['total_ipos']}")
for ipo in data['ipos']:
    print(f"  • {ipo['company_name']}")
```

#### Example 2: Get as JSON string

```python
from ipo_fetcher import get_ipo_data_json

# Get JSON formatted string
json_str = get_ipo_data_json(month=12, year=2025)
print(json_str)
```

#### Example 3: Save to file

```python
from ipo_fetcher import fetch_ipo_data
import json

data = fetch_ipo_data(month=12, year=2025)
with open('ipo_data.json', 'w') as f:
    json.dump(data, f, indent=2)
```

#### Example 4: Filter IPOs by criteria

```python
from ipo_fetcher import fetch_ipo_data

data = fetch_ipo_data(month=12, year=2025)

# Get only book-building IPOs (with price range)
book_building_ipos = [ipo for ipo in data['ipos'] if 'to' in ipo['price']]
print(f"Book Building IPOs: {len(book_building_ipos)}")

# Get only fixed price IPOs
fixed_price_ipos = [ipo for ipo in data['ipos'] if 'to' not in ipo['price']]
print(f"Fixed Price IPOs: {len(fixed_price_ipos)}")
```

#### Example 5: Loop through multiple months

```python
from ipo_fetcher import fetch_ipo_data

for month in range(1, 13):
    data = fetch_ipo_data(month=month, year=2025)
    print(f"{data['month_name']} 2025: {data['total_ipos']} IPOs")
```

## API Reference

### `fetch_ipo_data(month, year, use_selenium=True)`

Fetches IPO data for a specific month and year.

**Parameters:**
- `month` (int): Month number (1-12)
- `year` (int): Year (e.g., 2025)
- `use_selenium` (bool): Use Selenium for JavaScript rendering (default: True)

**Returns:** Dictionary with keys:
- `year`: Year of the data
- `month`: Month number
- `month_name`: Month name (e.g., "December")
- `total_ipos`: Number of IPOs in that month
- `ipos`: List of IPO dictionaries
- `error` (optional): Error message if data fetch failed

**Raises:**
- `ValueError`: If month is not between 1-12 or year is invalid

### `get_ipo_data_json(month, year)`

Convenience function that returns JSON string instead of dictionary.

**Parameters:**
- `month` (int): Month number (1-12)
- `year` (int): Year (e.g., 2025)

**Returns:** JSON formatted string

## Data Fields Explained

| Field | Description | Example |
|-------|-------------|---------|
| `company_name` | Name of the company issuing the IPO | "Meesho Ltd. IPO" |
| `open_date` | Date when IPO bidding opens (YYYY-MM-DD) | "2025-12-03" |
| `close_date` | Date when IPO bidding closes (YYYY-MM-DD) | "2025-12-05" |
| `list_date` | Date when shares are listed on exchange | "2025-12-10" or "Yet to list" |
| `price` | Issue price (fixed) or price range (book building) | "111.00" or "100.00 to 110.00" |
| `total_issue_amount` | Total monetary value of the IPO in Crores | "5,421.20" |
| `exchange` | Stock exchange(s) for listing | "BSE, NSE" |
| `lead_manager` | Lead manager/underwriter of the IPO | "Kotak Mahindra Capital" |

## Error Handling

The function returns a response even if there's an error:

```python
data = fetch_ipo_data(month=12, year=2025)
if 'error' in data:
    print(f"Error: {data['error']}")
else:
    print(f"Successfully fetched {data['total_ipos']} IPOs")
```

## Notes

- The function filters IPOs based on the **close_date** falling in the specified month
- Dates are automatically parsed from the website format (e.g., "Mon, Dec 22, 2025")
- Selenium is used by default for better JavaScript content rendering
- Fallback to requests library is available by setting `use_selenium=False`
- All dates are returned in ISO 8601 format (YYYY-MM-DD)

## Troubleshooting

### "No IPO data table found on the webpage"
- The website structure may have changed
- Try using `use_selenium=False` parameter
- Check your internet connection

### Selenium issues
- Ensure ChromeDriver is installed and in PATH
- On Windows, you may need to download ChromeDriver separately
- Try using requests-based fetching: `fetch_ipo_data(month=12, year=2025, use_selenium=False)`

### Rate limiting
- Add delays between multiple requests if fetching many months:
```python
import time
for month in range(1, 13):
    data = fetch_ipo_data(month=month, year=2025)
    time.sleep(2)  # 2 second delay
```

## License

This tool is provided for educational purposes. Please respect the website's terms of service and robots.txt when scraping.

## Support

For issues or questions, refer to the example files:
- `example_usage.py` - Complete usage examples
- `ipo_fetcher.py` - Main module with detailed docstrings
