"""Intended to
1) request to web api to get STRUCTURED text
2) pdf -> text file (key:value pair) - potentially as JSON.
3) store each text file.
"""

import time

from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()


def get_pdf_link(ticker: str, year: int):
    url = f"https://www.nzx.com/companies/{ticker}/announcements?code={ticker}&year={year}"
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        memo = link.find_next_sibling("span")
        if memo is None:
            continue

        if memo.get_text(strip=True) in ["ANNREP", "FLLYR"]:
            relative_path = link.get("href")
            assert isinstance(relative_path, str)
            return "https://www.nzx.com" + relative_path

    return None


print(get_pdf_link("AIA", 2024))
