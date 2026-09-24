"""Intended to
1) request to web api to get STRUCTURED text
2) pdf -> text file (key:value pair) - potentially as JSON.
3) store each text file.
"""

import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()


def get_report_link(ticker: str, year: int):
    url = f"https://www.nzx.com/companies/{ticker}/announcements?code={ticker}&year={year}"
    driver.get(url)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.find_all("a", href=True)
    for link in links:
        report_code = link.find_next_sibling("span")
        if report_code is None:
            continue

        if report_code.get_text(strip=True) in ["ANNREP", "FLLYR"]:
            relative_path = link.get("href")
            assert isinstance(relative_path, str)
            return "https://www.nzx.com" + relative_path

    return None


def web_scrape(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    main_paragraph = soup.find("p", class_="whitespace-pre-line")
    assert main_paragraph is not None
    return main_paragraph.get_text(strip=True)
