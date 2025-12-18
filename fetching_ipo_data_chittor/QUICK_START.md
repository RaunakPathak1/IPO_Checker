# IPO Fetcher - Quick Start Guide

## Installation
Already done! Your requirements.txt has all needed packages.

## Quick Usage (Copy & Paste)

### Get IPO data for a specific month
```python
from ipo_fetcher import fetch_ipo_data
import json

# Fetch December 2025
data = fetch_ipo_data(month=12, year=2025)
print(json.dumps(data, indent=2))
```

### Get IPO data for multiple months
```python
from ipo_fetcher import fetch_ipo_data

for month in range(1, 13):  # All 12 months
    data = fetch_ipo_data(month=month, year=2025)
    print(f"{data['month_name']}: {data['total_ipos']} IPOs")
```

### Save to JSON file
```python
from ipo_fetcher import fetch_ipo_data
import json

data = fetch_ipo_data(month=12, year=2025)
with open('ipo_dec_2025.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Filter by criteria
```python
from ipo_fetcher import fetch_ipo_data

data = fetch_ipo_data(month=12, year=2025)

# Only book-building IPOs (with price range)
book_building = [ipo for ipo in data['ipos'] if 'to' in ipo['price']]

# Only from specific exchange
nse_ipos = [ipo for ipo in data['ipos'] if 'NSE' in ipo['exchange']]
```

## Function Signature

```python
fetch_ipo_data(
    month: int,           # 1-12
    year: int,            # e.g., 2025
    use_selenium: bool=True  # Use Selenium for JS rendering
) -> dict
```

## Return Structure

```
{
  "year": int,
  "month": int,
  "month_name": str,
  "total_ipos": int,
  "ipos": [
    {
      "company_name": str,
      "open_date": "YYYY-MM-DD",
      "close_date": "YYYY-MM-DD",
      "list_date": "YYYY-MM-DD" or "Yet to list",
      "price": str,
      "total_issue_amount": str,
      "exchange": str,
      "lead_manager": str
    },
    ...
  ]
}
```

## Common Patterns

### Check if data fetch succeeded
```python
data = fetch_ipo_data(12, 2025)
if 'error' in data:
    print(f"Failed: {data['error']}")
else:
    print(f"Success: {data['total_ipos']} IPOs")
```

### Get company names only
```python
data = fetch_ipo_data(12, 2025)
companies = [ipo['company_name'] for ipo in data['ipos']]
```

### Convert to DataFrame
```python
import pandas as pd
from ipo_fetcher import fetch_ipo_data

data = fetch_ipo_data(12, 2025)
df = pd.DataFrame(data['ipos'])
```

### Export to CSV
```python
import pandas as pd
from ipo_fetcher import fetch_ipo_data

data = fetch_ipo_data(12, 2025)
df = pd.DataFrame(data['ipos'])
df.to_csv('ipo_data.csv', index=False)
```

## Use with Notebooks

In your Jupyter notebooks (chittor.ipynb or ipo_checker.ipynb):

```python
# Add this at the top
import sys
sys.path.append('/path/to/IPO_Checker')
from ipo_fetcher import fetch_ipo_data
import json

# Then use normally
data = fetch_ipo_data(month=12, year=2025)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No IPO data table found" | Try `use_selenium=False` |
| Slow response | Add delays between requests |
| Encoding errors | Make sure UTF-8 encoding is set |
| Selenium errors | Check ChromeDriver is installed |

## Performance Notes

- First call may be slow due to Selenium startup (~3-5 seconds)
- Subsequent calls are faster
- For batch operations, consider caching results

## All Available Functions

```python
from ipo_fetcher import:
  fetch_ipo_data()      # Main function
  get_ipo_data_json()   # Returns JSON string
```

## Examples File

See `example_usage.py` for 6 complete working examples.

## Full Documentation

See `IPO_FETCHER_README.md` for comprehensive documentation.
