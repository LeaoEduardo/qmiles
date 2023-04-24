from src.scrapers.models import *
from random import choice
import traceback
import multiprocessing as mp

from pprint import pprint
import pandas as pd

site_to_ws_class = {
  "decolar": DecolarWebScraper,
  "google_flights": GoogleFlightsWebScraper,
  "skyscanner": SkyscannerWebScraper,
  "voeazul": VoeAzulWebScraper,
  "voelivre": VoeLivreWebScraper,
  "smiles": SmilesWebScraper,
  "latampass": LatamPassWebScraper
}

workers = mp.cpu_count() - 1

def scrap_single_site(site_name):
  try:
    ws = site_to_ws_class[site_name](**kwargs)
    return ws.scrap_website()
  except Exception:
    traceback.print_exc()
    print(f"{site_name} failed")
    return []

def scraping_entrypoint(**kwargs):
  pprint(kwargs)
  results = []

  with mp.Pool(workers) as p:
    results = p.map(scrap_single_site, kwargs["sites"])
    
  return [result for site_results in results for result in site_results ]

format_number = lambda number: number if len(number)==2 else f"0{number}"

month = format_number(choice([str(m) for m in range(6,12)]))
arrival_day = format_number(choice([str(m) for m in range(1,15)]))
departure_day = format_number(choice([str(d + int(arrival_day)) for d in range(4,13)]))
minors_amount = choice([i for i in range(0,4)])

kwargs = {
  "sites": (
    "decolar",
    "voelivre",
    "google_flights",
    "voeazul",
    "smiles",
  ),
  
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

df = pd.DataFrame(scraping_entrypoint(**kwargs)).dropna(subset=["total_price"])
df["total_price"] = pd.to_numeric(df.total_price)
sorted_df = df.sort_values(by=["total_price"])
print(sorted_df.head())
sorted_df.to_csv("report.csv")
