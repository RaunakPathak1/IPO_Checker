"""
IPO Fetcher - Usage Examples

This script demonstrates how to use the ipo_fetcher module to fetch IPO data
from the Chittorgarh website in JSON format.
"""

from fetching_ipo_data_chittor.ipo_fetcher import fetch_ipo_data, get_ipo_data_json
import json

# Example 1: Fetch December 2025 IPO data as dictionary
print("=" * 70)
print("EXAMPLE 1: Fetch December 2025 IPO data")
print("=" * 70)
december_data = fetch_ipo_data(month=12, year=2025)
print(f"Total IPOs in December 2025: {december_data['total_ipos']}")
for ipo in december_data['ipos'][:3]:  # Show first 3
    print(f"\n  • {ipo['company_name']}")
    print(f"    Close Date: {ipo['close_date']}")
    print(f"    Price: {ipo['price']}")
    print(f"    Amount: {ipo['total_issue_amount']} Cr")

# Example 2: Fetch as JSON string
print("\n" + "=" * 70)
print("EXAMPLE 2: Get November 2025 data as JSON string")
print("=" * 70)
november_json = get_ipo_data_json(month=11, year=2025)
# Print first 500 characters
print(november_json[:500] + "...")

# Example 3: Loop through multiple months
print("\n" + "=" * 70)
print("EXAMPLE 3: Fetch data for multiple months")
print("=" * 70)
for month in [10, 11, 12]:
    data = fetch_ipo_data(month=month, year=2025)
    print(f"  {data['month_name']} 2025: {data['total_ipos']} IPOs")

# Example 4: Save to file
print("\n" + "=" * 70)
print("EXAMPLE 4: Save IPO data to JSON file")
print("=" * 70)
data = fetch_ipo_data(month=12, year=2025)
with open('ipo_december_2025.json', 'w') as f:
    json.dump(data, f, indent=2)
print("✓ Data saved to ipo_december_2025.json")

# Example 5: Filter specific IPOs
print("\n" + "=" * 70)
print("EXAMPLE 5: Filter IPOs by price range")
print("=" * 70)
data = fetch_ipo_data(month=12, year=2025)
high_price_ipos = [ipo for ipo in data['ipos'] 
                   if 'to' in ipo['price']]  # Book building IPOs
print(f"Book Building IPOs in December: {len(high_price_ipos)}")
for ipo in high_price_ipos[:2]:
    print(f"  • {ipo['company_name']}: {ipo['price']}")

# Example 6: Error handling with invalid input
print("\n" + "=" * 70)
print("EXAMPLE 6: Error handling")
print("=" * 70)
try:
    invalid_data = fetch_ipo_data(month=13, year=2025)  # Invalid month
except ValueError as e:
    print(f"✓ Caught error: {e}")

print("\n" + "=" * 70)
print("All examples completed successfully!")
print("=" * 70)
