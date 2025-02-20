"""Boerse Frankfurt module."""
from datetime import datetime
import requests
# Import utils
try:
    from market import utils
except ImportError:
    import utils


def borsa_milano(
        ticker: str, start_date: str | None = None, end_date: str | None = None
    ) -> list:
    """
    Fetches historical market data for a given ticker symbol from the Borsa Italiana API.

    Args:
        ticker (str): The ticker symbol of the financial instrument.

    Returns:
        list: A list of dictionaries containing historical market data start from 5 years ago to today in the following format:
            {'date': 'yyyy-mm-dd', 'marketPrice': float}
    """
    # Get market data
    url = 'https://charts.borsaitaliana.it/charts/services/ChartWService.asmx/GetPrices'

    headers = {
        'User-Agent': utils.get_random_user_agent(),
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://charts.borsaitaliana.it",
        "Referer": f"https://charts.borsaitaliana.it/charts/Bit/SummaryChart.aspx?code={ticker}&lang=it",
        "X-Requested-With": "XMLHttpRequest",
    }

    # Payload della richiesta
    payload = {
        "request": {
            "SampleTime": "1d",  # Intervallo di campionamento (1 giorno)
            "TimeFrame": "5y",  # Intervallo temporale (ultimi 5 anni)
            "RequestedDataSetType": "ohlc",  # Tipo di dati (Open, High, Low, Close)
            "ChartPriceType": "price",  # Tipo di prezzo
            "Key": f"{ticker}.MOT",  # Codice ISIN con suffisso
            "OffSet": 0,
            "FromDate": None,  # Nessuna data di inizio specificata
            "ToDate": None,  # Nessuna data di fine specificata
            "UseDelay": False,  # Nessun ritardo
            "KeyType": "Topic",
            "KeyType2": "Topic",
            "Language": "it-IT",  # Lingua italiana
        }
    }

    # Invia la richiesta POST
    response = requests.post(
        url, 
        headers=headers, 
        json=payload
    )

    # Controlla lo stato della risposta
    if response.status_code == 200:
        # Decodifica i dati JSON
        data = response.json()
    # Estrai i dati OHLC
        prices = data.get("d", [])  # `d` è una lista di liste

        # Converte i dati nel formato richiesto
        market_data = []
        for item in prices:
            timestamp = item[0]  # Timestamp in millisecondi
            close_price = item[4]  # Prezzo di chiusura (Close)

            # Converti il timestamp in una data leggibile
            date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

            # Aggiungi al formato richiesto
            market_data.append({"date": date, "marketPrice": close_price})
    
    # Fill missing dates
    market_data = utils.fill_missing_dates(market_data, start_date=start_date, end_date=end_date)

    return market_data


def main() -> None:
    """Main function for local tests only."""
    utils.print_list(borsa_milano("IT0005415291"))


if __name__ == "__main__":
    main()
