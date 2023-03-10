from src.scrapers.models import *

site_to_ws_class = {
  "decolar": DecolarWebScraper,
  "google_flights": GoogleFlightsWebScraper,
  "skyscanner": SkyscannerWebScraper
}

def scraping_entrypoint(**kwargs):
  results = []
  for site_name, url in kwargs["urls"].items():
    ws = site_to_ws_class[site_name](**kwargs)
    results.append(ws.scrap_website(url, site_name))
  return results

kwargs = {
  "urls": {
    "decolar": "https://decolar.com/passagens-aereas/",
    "google_flights": "https://www.google.com/flights?hl=pt-BR",
    "skyscanner": "https://www.skyscanner.net/transport/flights"
  },
  
  "arrival_date": "2023-05-20",
  "departure_date": "2023-05-25",
  "origin_city": "SAO",
  "destiny_city": "ORL",
  "guests": {
    "adults": 2,
    "minors": {
      "amount": 1,
      "ages": [1, 5, 15]
    },
    "class": "economy"
  },
  "check_in_luggage": True,
  "max_stops": 0
}

# ws = DecolarWebScraper(**kwargs)
# print("scraping decolar...")
# print(ws.scrap_website("https://decolar.com/passagens-aereas", "decolar"))

# ws = GoogleFlightsWebScraper(**kwargs)
# print("scraping google flights...")
# print(ws.scrap_website("https://www.google.com/flights?hl=pt-BR", "google_flights"))

# ws = SkyscannerWebScraper(**kwargs)
# print("scraping Skyscanner...")
# print(ws.scrap_website("https://www.skyscanner.net/transport/flights", "skyscanner"))

ws = VoeLivreWebScraper(**kwargs)
print("scraping VoeLivre...")
print(ws.scrap_website("https://www.voelivre.com.br/passagens-aereas/pesquisa/RIO/ORL/2023-06-15/ORL/RIO/2023-06-22/?a=2&c=1&c=0#", "voelivre"))


# response = scraping_entrypoint(**kwargs)
