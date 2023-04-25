import os
import sys
sys.path.append(os.getcwd())
from src.web_scraper import scraping_entrypoint

def test_scrap_single_url():
  kwargs = {
    "urls": {
      # "decolar": "https://decolar.com"
      "google_flights": "https://www.google.com/flights?hl=pt-BR"
    },
    
    "arrival_date": "2023-03-20",
    "departure_date": "2023-03-30",
    "origin_city": "Rio de Janeiro",
    "destiny_city": "Orlando",
    "guests": {
      "adults": 2,
      "minors": {
        "amount": 1,
        "ages": [15]
      },
      "class": "business"
    },
    "check_in_luggage": True,
    "one_stop": True
  }

  response = scraping_entrypoint(**kwargs)

  assert isinstance(response, list)
  # assert isinstance(response[0], dict)
  # assert "price_by_adult" in response[0]
  # assert "price_without_taxes" in response[0]
  # assert "price_taxes" in response[0]
  # assert "price_total" in response[0]
  # assert "outbound_company" in response[0]
  # assert "outbound_departure_hour" in response[0]
  # assert "outbound_arrival_hour" in response[0]
  # assert "outbound_stops" in response[0]
  # assert "outbound_flight_duration" in response[0]
  # assert "return_company" in response[0]
  # assert "return_departure_hour" in response[0]
  # assert "return_arrival_hour" in response[0]
  # assert "return_stops" in response[0]
  # assert "return_flight_duration" in response[0]
  # assert "site_name" in response[0]
  # assert "page_url" in response[0]