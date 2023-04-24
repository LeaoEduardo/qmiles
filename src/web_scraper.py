from src.scrapers.models import *
from random import choice
import traceback

from pprint import pprint

site_to_ws_class = {
  "decolar": DecolarWebScraper,
  "google_flights": GoogleFlightsWebScraper,
  "skyscanner": SkyscannerWebScraper,
  "voeazul": VoeAzulWebScraper,
  "voelivre": VoeLivreWebScraper,
  "smiles": SmilesWebScraper,
  "latampass": LatamPassWebScraper
}

def scraping_entrypoint(**kwargs):
  pprint(kwargs)
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
    "google_flights": "https://www.google.com/flights?hl=pt-BR",
    "voeazul": "https://www.voeazul.com.br/br/pt/home/selecao-voo?",
    # "latampass": "https://latampass.latam.com/pt_br/",
    "smiles": "https://www.smiles.com.br/mfe/emissao-passagem?tripType=1",
    # "skyscanner": "https://www.skyscanner.net/transport/flights",
  },
  
  "arrival_date": f"2023-{month}-{arrival_day}",
  "departure_date": f"2023-{month}-{departure_day}",
  "origin_city": choice([
    "GRU", "GIG", 
    "BHZ", "BSB", "CWB"
  ]),
  "destiny_city": choice([
    "MCO", 
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
  # "check_in_luggage": choice((True, False)),
  # "max_stops": choice((0,1))
}

print(scraping_entrypoint(**kwargs))
