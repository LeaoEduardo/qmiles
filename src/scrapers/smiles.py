import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

from src.scrapers.base import BaseWebScraper

class SmilesWebScraper(BaseWebScraper):
  xpaths = {
    "close_login_popup": "/html/body/div[8]/div/nav/div[6]/div[1]/i",
    "close_ok_popup": "/html/body/div[17]/md-dialog/md-dialog-content/div[2]/div/div/div/button"
  }

  delay = 120

  def __init__(self, **kwargs):
    super().__init__(**kwargs, xpaths=self.xpaths, delay=self.delay)
    self.base_url = "https://www.smiles.com.br/mfe/emissao-passagem?tripType=1"
  
  def insert_cities(self):
    codes_df = pd.read_csv("src/ip2location-iata-icao-master/iata-icao.csv")

    def get_abbreviation(name: str):
      if len(codes_df[codes_df["iata"] == name]):
        return name
      else:
        raise ValueError(f"City {name} invalid!")

    self.origin_city, self.destiny_city = get_abbreviation(self.origin_city), get_abbreviation(self.destiny_city)

    self.base_url = "&".join([
                                self.base_url, 
                                f"originAirport={self.origin_city}", 
                                f"destinationAirport={self.destiny_city}",
    ])
                                  
  def insert_dates(self):

    convert_to_miliseconds = lambda date: int(datetime.fromisoformat(date).timestamp()*1000)
    self.base_url = "&".join([
                      self.base_url,
                      f"departureDate={convert_to_miliseconds(self.arrival_date)}",
                      f"returnDate={convert_to_miliseconds(self.departure_date)}",
    ])

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

    query_parameters = f"adults={paying_adults}&children={paying_minors}&infants={paying_babies}"

    self.base_url = "&".join([self.base_url, query_parameters])

  def get_results(self, site_name) -> dict:

    def get_info_from_container(container, prefix) -> dict:
      info = {}
      info_elem = container.find_elements(By.CLASS_NAME, "select-flight-list-accordion-item")[0]
      info[f"{prefix}_company"] = info_elem.find_element(By.CLASS_NAME, "company").get_attribute("innerHTML")
      info[f"{prefix}_departure_hour"] = info_elem.find_elements(By.CLASS_NAME, "iata-code")[0].find_element(By.XPATH, "strong").text
      info[f"{prefix}_arrival_hour"] = info_elem.find_elements(By.CLASS_NAME, "iata-code")[1].find_element(By.XPATH, "strong").text
      info[f"{prefix}_flight_duration"] = info_elem.find_element(By.CLASS_NAME, "scale-duration__time").text
      info[f"{prefix}_stops"] = info_elem.find_element(By.CLASS_NAME, "scale-duration__type-flight").text
      info[f"{prefix}_miles"] = info_elem.find_element(By.CLASS_NAME, "miles").find_element(By.XPATH, "strong").text.rstrip("milhas").replace(".","")
      return info
    
    return_button_elem = self.find_element(By.ID, "select-flight-accordion-volta")
    time.sleep(5)
    self.click_on_element(return_button_elem)
    time.sleep(5)
    if len(self.driver.find_elements(By.CLASS_NAME, "select-flight-not-found-card")):
      print("No flights found for this date!")
      return []
    outbound_container_elem = self.find_element(By.CLASS_NAME, "list-ida")
    return_container_elem = self.find_element(By.CLASS_NAME, "list-volta")
    results = get_info_from_container(outbound_container_elem, "outbound") | get_info_from_container(return_container_elem, "return")
    results["total_miles"] = str(int(results.pop("return_miles")) + int(results.pop("outbound_miles")))
    results["page_url"] = self.base_url

    return [results]

  def scrap_website(self, url, site_name):
    self.insert_cities()
    self.insert_dates()
    self.select_guests()
    self.driver.get(self.base_url)

    return self.get_results(site_name)