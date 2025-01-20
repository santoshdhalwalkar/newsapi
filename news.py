import certifi
import ssl
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

from newsapi import NewsApiClient


# Initialize NewsAPI client
newsapi = NewsApiClient(api_key="0f912b6d3e8d4dce900cb30b6478f6dc")

try:
    # Fetch top headlines
    headlines = newsapi.get_top_headlines(language="en", country="us")
    print("NewsAPI Key is working!")
except Exception as e:
    print(f"Error with NewsAPI Key: {e}")
    print(f"Error with NewsAPI Key: {e}")