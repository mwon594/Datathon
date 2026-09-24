from dotenv import load_dotenv

from src.fileinterface import upload_file
from src.get_reports import get_report_link, web_scrape


def main(tickers: list[str], years: list[int]):
    successful_scrapes: list[tuple[str, int]] = []
    for ticker in tickers:
        for year in years:
            url = get_report_link(ticker, year)
            if url is None:
                print(f"No report found for {ticker} in {year}.")
                continue

            content = web_scrape(url)
            file_path = f"unstructured_data/{ticker}_{year}.txt"
            with open(file_path, "w") as file:
                file.write(content)

            successful_scrapes.append((ticker, year))
            print(f"Report for {ticker} in {year} saved to {file_path}.")

    for ticker, year in successful_scrapes:
        file_path = f"unstructured_data/{ticker}_{year}.txt"
        upload_file(file_path)


if __name__ == "__main__":
    load_dotenv()
    tickers = ["FPH", "MEL", "IFT", "AIA", "FCG", "MCY", "CEN", "MFT", "ATM", "POT"]
    years = [2026, 2025, 2024, 2023, 2022, 2021, 2020]
    main(tickers, years)
