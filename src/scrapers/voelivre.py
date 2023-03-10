import os
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

from src.scrapers.base import BaseWebScraper

class VoeLivreWebScraper(BaseWebScraper):
  xpaths = {
    "close_login_popup": "/html/body/div[8]/div/nav/div[6]/div[1]/i",
    "close_ok_popup": "/html/body/div[17]/md-dialog/md-dialog-content/div[2]/div/div/div/button"
  }

  def __init__(self, **kwargs):
    super().__init__(**kwargs, xpaths=self.xpaths)
    self.base_url = "https://www.voelivre.com.br/passagens-aereas/pesquisa/"
  
  def insert_cities(self):
    codes_df = pd.read_csv("src/ip2location-iata-icao-master/iata-icao.csv")

    def get_abbreviation(name: str):
      if len(codes_df[codes_df["iata"] == name]):
        return name
      else:
        raise ValueError(f"City {name} invalid!")

    self.origin_city, self.destiny_city = get_abbreviation(self.origin_city), get_abbreviation(self.destiny_city)

    self.base_url = os.path.join(
                                  self.base_url, 
                                  self.origin_city, 
                                  self.destiny_city,
                                  "arrival_date",
                                  self.destiny_city,
                                  self.origin_city, 
                                  "departure_date",
                                )

  def insert_dates(self):
    self.base_url = self.base_url.\
                      replace("arrival_date", self.arrival_date).\
                      replace("departure_date", self.departure_date)

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

    query_parameters = f"?a={paying_adults}&c={paying_minors}&c={paying_babies}#"

    self.base_url = os.path.join(self.base_url,query_parameters)
    
  def apply_filters(self):
    if self.max_stops != -1:
      filter_stops = self.find_element(By.ID, "paradas_collapse")
      stop_options = filter_stops.find_elements(By.CLASS_NAME, "md-container")
      self.click_on_element(stop_options[self.max_stops])

      return_stops = filter_stops.find_element(By.XPATH, "ul/li[2]/a")
      self.click_on_element(return_stops)
      time.sleep(2)
      stop_options = filter_stops.find_elements(By.CLASS_NAME, "md-container")
      self.click_on_element(stop_options[self.max_stops])

  def get_results(self, site_name) -> dict:
    max_results = 3
    results_list = []
    clusters = self.driver.find_element(By.ID, "clusters")
    total_price_list = clusters.find_elements(By.CLASS_NAME, "price-amount")[:max_results]
    itineraries_containers = clusters.find_elements(By.CLASS_NAME, "itineraries-container")[:max_results]
    
    if len(total_price_list) != len(itineraries_containers):
      raise Exception("BUG in results selection: len(total_price_list) != len(itineraries_containers)")

    for i, container in enumerate(itineraries_containers):
      result = {}
      sub_cluster = container.find_elements(By.CLASS_NAME, "sub-cluster")
      outbound_info = sub_cluster[0]
      return_info = sub_cluster[1]
      
      result["total_price"] = total_price_list[i].text
      result["outbound_company"] = outbound_info.find_element(By.CLASS_NAME, "airlines").text
      result["outbound_departure_hour"] = outbound_info.find_element(By.CLASS_NAME, "leave").find_element(By.CLASS_NAME, "hour").text
      result["outbound_arrival_hour"] = outbound_info.find_element(By.CLASS_NAME, "arrive").find_element(By.CLASS_NAME, "hour").text
      result["outbound_flight_duration"] = outbound_info.find_element(By.CLASS_NAME, "best-duration").text
      result["outbound_stops"] = outbound_info.find_element(By.CLASS_NAME, "stops-text").text
      result["return_company"] = return_info.find_element(By.CLASS_NAME, "airlines").text
      result["return_departure_hour"] = return_info.find_element(By.CLASS_NAME, "leave").find_element(By.CLASS_NAME, "hour").text
      result["return_arrival_hour"] = return_info.find_element(By.CLASS_NAME, "arrive").find_element(By.CLASS_NAME, "hour").text
      result["return_flight_duration"] = outbound_info.find_element(By.CLASS_NAME, "best-duration").text
      result["return_stops"] = return_info.find_element(By.CLASS_NAME, "stops-text").text
      result["page_url"] = self.base_url
      results_list.append(result)

    return results_list

  def scrap_website(self, url, site_name):
    self.insert_cities()
    self.insert_dates()
    self.select_guests()
    self.driver.get(self.base_url)
    # try:
    #   close_ok_popup_elem = self.find_element_by_xpath('close_ok_popup')
    #   self.click_on_element(close_ok_popup_elem)
    # except TimeoutException:
    #   print("Ok popup did not show.")
    self.apply_filters()
    time.sleep(100)
    return "Yes"
    # return self.get_results(site_name)