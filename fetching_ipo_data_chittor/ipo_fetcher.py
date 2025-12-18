import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict, Any
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_ipo_data(month: int, year: int, use_selenium: bool = True) -> Dict[str, Any]:
    """
    Fetch IPO details for a specific month and year from Chittorgarh website.
    
    Args:
        month (int): Month number (1-12)
        year (int): Year (e.g., 2025)
        use_selenium (bool): Whether to use Selenium for JavaScript rendering (default: True)
    
    Returns:
        Dict containing IPO data in JSON format with the following structure:
        {
            'year': int,
            'month': int,
            'month_name': str,
            'total_ipos': int,
            'ipos': [
                {
                    'company_name': str,
                    'open_date': str (YYYY-MM-DD),
                    'close_date': str (YYYY-MM-DD),
                    'list_date': str (YYYY-MM-DD) or 'Yet to list',
                    'price': str (price range or fixed price),
                    'total_issue_amount': str,
                    'exchange': str,
                    'lead_manager': str
                },
                ...
            ]
        }
    """
    
    # Validate month and year
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")
    if year < 2000 or year > 2100:
        raise ValueError(f"Invalid year: {year}. Year must be between 2000 and 2100.")
    
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Construct URL
    url = f"https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/mainboard/?year={year}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        if use_selenium:
            return _fetch_with_selenium(url, month, year, month_names)
        else:
            return _fetch_with_requests(url, month, year, month_names, headers)
    
    except Exception as e:
        return {
            'year': year,
            'month': month,
            'month_name': month_names[month],
            'total_ipos': 0,
            'ipos': [],
            'error': f'Failed to fetch data: {str(e)}'
        }


def _fetch_with_selenium(url: str, month: int, year: int, month_names: Dict) -> Dict[str, Any]:
    """Fetch data using Selenium to render JavaScript content."""
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Wait for table to load
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the main table
        table = soup.find('table')
        
        if not table:
            return {
                'year': year,
                'month': month,
                'month_name': month_names[month],
                'total_ipos': 0,
                'ipos': [],
                'error': 'No IPO data table found on the webpage'
            }
        
        ipos = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all('td')
            
            if len(cells) >= 8:  # Ensure we have all required columns
                try:
                    company_name = cells[0].get_text(strip=True)
                    open_date_text = cells[1].get_text(strip=True)
                    close_date_text = cells[2].get_text(strip=True)
                    list_date_text = cells[3].get_text(strip=True)
                    price = cells[4].get_text(strip=True)
                    total_issue = cells[5].get_text(strip=True)
                    exchange = cells[6].get_text(strip=True)
                    lead_manager = cells[7].get_text(strip=True) if len(cells) > 7 else ''
                    
                    # Parse dates and check if they belong to the specified month
                    open_date = _parse_date(open_date_text, year)
                    close_date = _parse_date(close_date_text, year)
                    list_date = _parse_date(list_date_text, year) if list_date_text and list_date_text != 'Yet to list' else 'Yet to list'
                    
                    # Filter by month - check if close_date falls in the specified month
                    if open_date and close_date:
                        if close_date.month == month:
                            ipos.append({
                                'company_name': company_name,
                                'open_date': open_date.strftime('%Y-%m-%d'),
                                'close_date': close_date.strftime('%Y-%m-%d'),
                                'list_date': list_date.strftime('%Y-%m-%d') if list_date != 'Yet to list' else 'Yet to list',
                                'price': price,
                                'total_issue_amount': total_issue,
                                'exchange': exchange,
                                'lead_manager': lead_manager
                            })
                except (ValueError, AttributeError, IndexError):
                    # Skip rows with parsing errors
                    continue
        
        return {
            'year': year,
            'month': month,
            'month_name': month_names[month],
            'total_ipos': len(ipos),
            'ipos': ipos
        }
    
    finally:
        driver.quit()


def _fetch_with_requests(url: str, month: int, year: int, month_names: Dict, headers: Dict) -> Dict[str, Any]:
    """Fetch data using requests library."""
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main table containing IPO data
    table = soup.find('table')
    
    if not table:
        return {
            'year': year,
            'month': month,
            'month_name': month_names[month],
            'total_ipos': 0,
            'ipos': [],
            'error': 'No IPO data table found on the webpage'
        }
    
    ipos = []
    rows = table.find_all('tr')[1:]  # Skip header row
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) >= 8:  # Ensure we have all required columns
            try:
                company_name = cells[0].get_text(strip=True)
                open_date_text = cells[1].get_text(strip=True)
                close_date_text = cells[2].get_text(strip=True)
                list_date_text = cells[3].get_text(strip=True)
                price = cells[4].get_text(strip=True)
                total_issue = cells[5].get_text(strip=True)
                exchange = cells[6].get_text(strip=True)
                lead_manager = cells[7].get_text(strip=True) if len(cells) > 7 else ''
                
                # Parse dates and check if they belong to the specified month
                open_date = _parse_date(open_date_text, year)
                close_date = _parse_date(close_date_text, year)
                list_date = _parse_date(list_date_text, year) if list_date_text and list_date_text != 'Yet to list' else 'Yet to list'
                
                # Filter by month - check if close_date falls in the specified month
                if open_date and close_date:
                    if close_date.month == month:
                        ipos.append({
                            'company_name': company_name,
                            'open_date': open_date.strftime('%Y-%m-%d'),
                            'close_date': close_date.strftime('%Y-%m-%d'),
                            'list_date': list_date.strftime('%Y-%m-%d') if list_date != 'Yet to list' else 'Yet to list',
                            'price': price,
                            'total_issue_amount': total_issue,
                            'exchange': exchange,
                            'lead_manager': lead_manager
                        })
            except (ValueError, AttributeError, IndexError):
                # Skip rows with parsing errors
                continue
    
    return {
        'year': year,
        'month': month,
        'month_name': month_names[month],
        'total_ipos': len(ipos),
        'ipos': ipos
    }


def _parse_date(date_str: str, year: int) -> datetime:
    """
    Parse date string in format 'Mon, Dec 22, 2025' to datetime object.
    
    Args:
        date_str (str): Date string to parse
        year (int): Default year if not present in string
    
    Returns:
        datetime object or None if parsing fails
    """
    date_str = date_str.strip()
    
    if not date_str:
        return None
    
    try:
        # Try parsing with year
        return datetime.strptime(date_str, '%a, %b %d, %Y')
    except ValueError:
        try:
            # Try parsing without year
            parsed = datetime.strptime(date_str, '%a, %b %d')
            return parsed.replace(year=year)
        except ValueError:
            return None


def get_ipo_data_json(month: int, year: int) -> str:
    """
    Get IPO data as a JSON string.
    
    Args:
        month (int): Month number (1-12)
        year (int): Year (e.g., 2025)
    
    Returns:
        str: JSON formatted string of IPO data
    """
    data = fetch_ipo_data(month, year)
    return json.dumps(data, indent=2)


# if __name__ == "__main__":
#     # Example usage
#     print("Fetching December 2025 IPO data...")
#     data = fetch_ipo_data(12, 2025)
#     print(json.dumps(data, indent=2))
    
#     print("\n" + "="*50 + "\n")
#     print("Fetching November 2025 IPO data...")
#     data = fetch_ipo_data(11, 2025)
#     print(json.dumps(data, indent=2))
