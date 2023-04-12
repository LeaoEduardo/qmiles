import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

from src.scrapers.base import BaseWebScraper

class VoeAzulWebScraper(BaseWebScraper):  
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.base_url = "https://www.voeazul.com.br/br/pt/home/selecao-voo?"
  
  def insert_cities(self):
    codes_df = pd.read_csv("src/ip2location-iata-icao-master/iata-icao.csv")

    def get_abbreviation(name: str):
      if len(codes_df[codes_df["iata"] == name]):
        return name
      else:
        raise ValueError(f"City {name} invalid!")

    self.origin_city, self.destiny_city = get_abbreviation(self.origin_city), get_abbreviation(self.destiny_city)

    self.base_url = self.base_url + "&".join([                                
                                f"c[0].ds={self.origin_city}", 
                                "arrival_date",
                                f"c[0].as={self.destiny_city}",
                                f"c[1].ds={self.destiny_city}", 
                                "departure_date",
                                f"c[1].as={self.origin_city}",
    ])
                                  
  def insert_dates(self):
    convert_date = lambda date: datetime.fromisoformat(date).strftime("%m/%d/%Y")
    self.base_url = self.base_url.\
                      replace("arrival_date", f"c[0].std={convert_date(self.arrival_date)}").\
                      replace("departure_date", f"c[1].std={convert_date(self.departure_date)}")
                      

  def select_guests(self):
    adult_price_age_lower_limit = 12
    baby_upper_limit = 1
    adults = self.guests["adults"]
    paying_adults = adults
    paying_minors = 0
    paying_babies = 0
    for minor_age in self.guests["minors"]["ages"]:
      if minor_age >= adult_price_age_lower_limit:
        paying_adults += 1
      elif minor_age <= baby_upper_limit:
        paying_babies += 1
      else:
        paying_minors += 1

    "p[0].t=ADT&p[0].c=2&p[0].cp=false&p[1].t=CHD&p[1].c=1&p[1].cp=false&p[2].t=INF&p[2].c=1&p[2].cp=false&f.dl=3&f.dr=3&cc=PTS"

    counter = 0
    query_parameters = "&".join([
                                    f"p[{counter}].t=ADT",
                                    f"p[{counter}].c={paying_adults}",
                                    f"p[{counter}].cp=false"
    ])
    counter += 1
    if paying_minors:
      query_parameters = "&".join([
                                    query_parameters,
                                    f"p[{counter}].t=CHD",
                                    f"p[{counter}].c={paying_minors}",
                                    f"p[{counter}].cp=false"
      ])
      counter += 1
    if paying_babies:
      query_parameters = "&".join([
                                    query_parameters,
                                    f"p[{counter}].t=INF",
                                    f"p[{counter}].c={paying_babies}",
                                    f"p[{counter}].cp=false"
      ])

    self.base_url = "&".join([self.base_url, query_parameters])

  def get_results(self, category) -> list[dict]:
    from itertools import product

    def get_info_from_container(container, prefix) -> list[dict]:
      infos = []
      info_elems = container.find_elements(By.CLASS_NAME, "flight-card")
      for info_elem in info_elems:
        info = {}
        info[f"{prefix}_company"] = "Azul"
        info[f"{prefix}_departure_hour"] = info_elem.find_element(By.CLASS_NAME, "departure").text.split("\n")[0]
        info[f"{prefix}_arrival_hour"] = info_elem.find_element(By.CLASS_NAME, "arrival").text.split("\n")[0]
        info[f"{prefix}_flight_duration"] = info_elem.find_element(By.CLASS_NAME, "duration").find_element(By.XPATH, "strong").text
        info[f"{prefix}_stops"] = info_elem.find_element(By.CLASS_NAME, "flight-leg-info").text.split("•")[0]
        info[f"{prefix}_{category}"] = info_elem.find_element(By.CLASS_NAME, "current").text.lstrip("R$").replace(".","").replace(",", ".")
        infos.append(info)
      return infos

    def blend_result(separated_result):
      result = separated_result[0] | separated_result[1]
      result[f"total_{category}"] = str(round(float(result.pop(f"return_{category}")) + float(result.pop(f"outbound_{category}"))))
      result["page_url"] = self.base_url
      return result
    

    try:
      failed_results_message = self.find_element(By.CLASS_NAME, "availability").find_element(By.XPATH, "div/div[1]/p").text
      print(category, failed_results_message)
      return None
    except NoSuchElementException:
      pass
      
    containers = self.driver.find_elements(By.CLASS_NAME, "trip-container")
    outbound_container = containers[0]
    return_container = containers[1]
    outbound_infos = get_info_from_container(outbound_container, "outbound")
    return_infos = get_info_from_container(return_container, "return")
    separated_results = product(outbound_infos, return_infos)

    return [blend_result(sr) for sr in separated_results]

  def scrap_website(self, url, site_name):
    self.insert_cities()
    self.insert_dates()
    self.select_guests()
    results = []
    for prefix, category in (("price", "BRL"), ("miles","PTS")):
      suffix = f"&cc={category}"
      self.driver.get(self.base_url+suffix)
      partial_results = self.get_results(prefix)
      if partial_results is None: continue
      results.extend(partial_results)

    return results