"""
IPO Fetcher - Chittorgarh.com IPO Data Scraper

A Python utility to fetch Indian IPO (Initial Public Offer) details from 
Chittorgarh.com and return the data in JSON format.

Usage:
    from fetching_ipo_data_chittor import fetch_ipo_data
    
    data = fetch_ipo_data(month=12, year=2025)
"""

from .ipo_fetcher import fetch_ipo_data, get_ipo_data_json

__version__ = "1.0.0"
__author__ = "IPO Fetcher"
__all__ = ["fetch_ipo_data", "get_ipo_data_json"]
