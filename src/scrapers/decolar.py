import os
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd

from src.scrapers.base import BaseWebScraper

class DecolarWebScraper(BaseWebScraper):
  xpaths = {
    "close_login_popup": "/html/body/div[8]/div/nav/div[6]/div[1]/i",
  }

  guest_classes_to_value = {
    "economy": "YC",
    "premium_economy": "PE",
    "business": "C",
    "first_class": "F",
  }

  def __init__(self, **kwargs):
    super().__init__(**kwargs, xpaths=self.xpaths, guest_classes_to_value=self.guest_classes_to_value)
    self.base_url = "https://www.decolar.com/shop/flights/results/roundtrip/"
  
  def insert_cities(self):
    codes_df = pd.read_csv("src/ip2location-iata-icao-master/iata-icao.csv")

    def get_abbreviation(name: str):
      if len(codes_df[codes_df["iata"] == name]):
        return name
      else:
        raise ValueError(f"City {name} invalid!")

    self.base_url = os.path.join(self.base_url, get_abbreviation(self.origin_city), get_abbreviation(self.destiny_city))

  def insert_dates(self):
    self.base_url = os.path.join(self.base_url, self.arrival_date, self.departure_date)

  def select_guests(self):
    adult_price_age_lower_limit = 12
    adults = self.guests["adults"]
    minors = self.guests["minors"]["amount"]
    paying_adults = adults
    paying_minors = 0
    for minor_age in self.guests["minors"]["ages"]:
      if minor_age >= adult_price_age_lower_limit:
        paying_adults += 1
      else:
        paying_minors += 1
    class_value = self.guest_classes_to_value[self.guests["class"]]

    minors_path_parameter = "-".join(["C" for _ in range(paying_minors)]) if paying_minors else "0"

    query_parameters = f"?from=SB&di={adults}-{minors}"
    if minors:
      query_parameters += ":" + "-".join([str(age) for age in self.guests["minors"]["ages"]])

    self.base_url = os.path.join(self.base_url,
                                 str(paying_adults), 
                                 minors_path_parameter,
                                 "0/NA/NA",
                                 class_value,
                                 "NA/NA",
                                 query_parameters
                                 )
    
  def apply_filters(self):
    if self.max_stops != -1:
      try:
        filter_stops = self.driver.find_element(By.ID, "filter-stops")
        filter_max_stops_elem = filter_stops.find_elements(By.CLASS_NAME, "filters-checkbox-left")[self.max_stops+1]
        self.click_on_element(filter_max_stops_elem)
        time.sleep(2)
      except (TimeoutException, NoSuchElementException):
        print("Could not apply max stops filter.")
    if self.check_in_luggage:
      try:
        filter_baggage = self.driver.find_element(By.ID, "filter-baggage")
        filter_check_in_luggage_elem = filter_baggage.find_elements(By.CLASS_NAME, "filters-checkbox-left")[-1]
        self.click_on_element(filter_check_in_luggage_elem)
        time.sleep(2)
      except (TimeoutException, NoSuchElementException):
        print("Could not apply check in luggage filter.")

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
    # self.apply_filters()
    return self.get_results(site_name)