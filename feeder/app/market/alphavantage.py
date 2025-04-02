"""Alphavantage module."""
from datetime import datetime
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils

def alphavantage(
        ticker: str, start_date: str | None = None, end_date: str | None = None, apikey: str | None = None
    ) -> list:
    """
    Fetches historical market data for a given ticker symbol from the Börse Frankfurt API.
    Args:
        ticker (str): The ticker symbol of the financial instrument.
        start_date (str, optional): The start date for data retrieval (YYYY-MM-DD format).
        end_date (str, optional): The end date for data retrieval (YYYY-MM-DD format).
        apikey (str, optional): The API key for authentication. If not provided, a default key is used.
    Returns:
        list: A list of dictionaries containing historical market data in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get market data
    url = 'https://www.alphavantage.co/query'
    query_params = {
        'function': 'TIME_SERIES_DAILY',
        'outputsize': 'full',
        'symbol': ticker,
        'apikey': apikey
    }
    headers = {
        'User-Agent': utils.get_random_user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://www.alphavantage.co',
        'Referer': 'https://www.alphavantage.co/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    response = requests.get(
        url,
        verify=False,
        params=query_params,
        headers=headers,
        timeout=10
    )
    
    # Extract the daily data.
    time_series = response.json()["Time Series (Daily)"]
    # Format the data into the required format.
    market_data = [{
        "date": date,
        "marketPrice": float(daily_data["4. close"])
    } for date, daily_data in time_series.items()]
    # Fill missing dates.
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)
    return market_data

def main() -> None:
    """Main function for local tests only."""
    utils.print_list(alphavantage("CBU2.DEX", start_date="2023-07-31", apikey="demo"))

if __name__ == "__main__":
    main()