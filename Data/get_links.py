"""Intended to
1) request to web api to get STRUCTURED text
2) pdf -> text file (key:value pair) - potentially as JSON.
3) store each text file.
"""

import requests
from bs4 import BeautifulSoup


def get_pdf_links(ticker: str, year: int):
    url = f"https://www.nzx.com/companies/{ticker}/announcements?code={ticker}&year={year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)
    print(len(links))
    counter = 0
    for link in links:
        print(link.get("href"))
        memo = link.find_next_sibling("span")
        if memo is None:
            continue

        counter += 1
        if memo.get_text(strip=True) in ["ANNREP", "FLLYR"]:
            return link.get("href")

    print(counter)
    return "Fail"


print(get_pdf_links("AIA", 2024))
