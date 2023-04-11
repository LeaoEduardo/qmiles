from src.scrapers.models import *
from random import choice
import traceback

site_to_ws_class = {
  "decolar": DecolarWebScraper,
  "google_flights": GoogleFlightsWebScraper,
  "skyscanner": SkyscannerWebScraper,
  "voelivre": VoeLivreWebScraper
}

def scraping_entrypoint(**kwargs):
  results = []
  for site_name, url in kwargs["urls"].items():
    try:
      ws = site_to_ws_class[site_name](**kwargs)
      results.extend(ws.scrap_website(url, site_name))
    except Exception:
      traceback.print_exc()
      print(f"{site_name} failed")
  return results

format_number = lambda number: number if len(number)==2 else f"0{number}"

month = format_number(choice([str(m) for m in range(6,12)]))
arrival_day = format_number(choice([str(m) for m in range(1,15)]))
departure_day = format_number(choice([str(d + int(arrival_day)) for d in range(4,13)]))
minors_amount = choice([i for i in range(0,4)])

kwargs = {
  "urls": {
    "decolar": "https://decolar.com/passagens-aereas/",
    "voelivre": "https://www.voelivre.com.br/passagens-aereas/pesquisa",
    # "google_flights": "https://www.google.com/flights?hl=pt-BR",
    # "skyscanner": "https://www.skyscanner.net/transport/flights",
  },
  
  "arrival_date": f"2023-{month}-{arrival_day}",
  "departure_date": f"2023-{month}-{departure_day}",
  "origin_city": choice([
    "SAO", "RIO", 
    "BHZ", "BSB", "CWB"
  ]),
  "destiny_city": choice([
    "ORL", 
    "LGA", "JFK", "DFW", 
    "MIA", "LAX"]),
  "guests": {
    "adults": choice([i for i in range(1,4)]),
    "minors": {
      "amount": minors_amount,
      "ages": [choice([i for i in range(1,18)]) for _ in range(minors_amount)]
    },
    "class": "economy"
  },
  "check_in_luggage": choice((True, False)),
  # "max_stops": choice((0,1))
}

# print(kwargs)

# ws = DecolarWebScraper(**kwargs)
# print("scraping decolar...")
# print(ws.scrap_website("https://decolar.com/passagens-aereas", "decolar"))

# ws = GoogleFlightsWebScraper(**kwargs)
# print("scraping google flights...")
# print(ws.scrap_website("https://www.google.com/flights?hl=pt-BR", "google_flights"))

# ws = SkyscannerWebScraper(**kwargs)
# print("scraping Skyscanner...")
# print(ws.scrap_website("https://www.skyscanner.net/transport/flights", "skyscanner"))
# import time
# time.sleep(100)

# ws = VoeLivreWebScraper(**kwargs)
# print("scraping VoeLivre...")
# print(ws.scrap_website("https://www.voelivre.com.br/passagens-aereas/pesquisa/RIO/ORL/2023-06-15/ORL/RIO/2023-06-22/?a=2&c=1&c=0#", "voelivre"))


print(scraping_entrypoint(**kwargs))
