''' Intended to 
1) request to web api to get STRUCTURED text
2) pdf -> text file (key:value pair) - potentially as JSON.
3) store each text file.
'''
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def get_pdf_links(base_url = ):
    response = requests.get(base_url)
