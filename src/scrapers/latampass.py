import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import pandas as pd

from src.scrapers.base import BaseWebScraper

class LatamPassWebScraper(BaseWebScraper):
  xpaths = {
    "close_login_popup": "/html/body/div[8]/div/nav/div[6]/div[1]/i",
    "close_ok_popup": "/html/body/div[17]/md-dialog/md-dialog-content/div[2]/div/div/div/button"
  }

  def __init__(self, **kwargs):
    super().__init__(**kwargs, xpaths=self.xpaths, delay=self.delay)
    self.base_url = "https://latampass.latam.com/pt_br/"
  
  def insert_cities(self):
    codes_df = pd.read_csv("src/ip2location-iata-icao-master/iata-icao.csv")

    def get_abbreviation(name: str):
      if len(codes_df[codes_df["iata"] == name]):
        return name
      else:
        raise ValueError(f"City {name} invalid!")

    self.origin_city, self.destiny_city = get_abbreviation(self.origin_city), get_abbreviation(self.destiny_city)

    origin_city_elem = self.find_element(By.ID, "irportorigemtext")
    self.click_on_element(origin_city_elem)
    origin_city_elem.send_keys(self.origin_city)
    time.sleep(2)
    origin_city_container = self.find_element(By.ID, "content_large_body_item_origem").find_elements(By.CLASS_NAME, "content_large_body_item_item")
    for elem in origin_city_container:
      if self.origin_city in elem.find_element(By.CLASS_NAME, "content_large_title").text:
        self.click_on_element(elem)

    destiny_city_elem = self.find_element(By.ID, "irportdestinationtext")
    self.click_on_element(destiny_city_elem)
    destiny_city_elem.send_keys(self.destiny_city)
    time.sleep(2)
    destiny_city_container = self.find_element(By.ID, "content_large_body_item_destination").find_elements(By.CLASS_NAME, "content_large_body_item_item")
    for elem in destiny_city_container:
      if self.destiny_city in elem.find_element(By.CLASS_NAME, "content_large_title").text:
        self.click_on_element(elem)
                                  
  def insert_dates(self):
    from babel.dates import format_date
    from datetime import date

    def select_date(current_month, current_year, target_month, target_year, target_day):
      left_elem = date_range_elem.find_element(By.CLASS_NAME, "left")
      while current_year > target_year or current_month != target_month:
        next_elem = date_range_elem.find_element(By.CLASS_NAME, "next")
        self.click_on_element((next_elem))
        time.sleep(1)
        left_elem = date_range_elem.find_element(By.CLASS_NAME, "left")
        current_month, current_year = left_elem.find_element(By.CLASS_NAME, "month").text.split(" ")
      available_days = left_elem.find_elements(By.CLASS_NAME, "available")
      for day in available_days:
        if day.text == str(target_day):
          self.click_on_element(day)
          break
      return current_month, current_year

    arrival_date = date.fromisoformat(self.arrival_date)
    departure_date = date.fromisoformat(self.departure_date)
    arrival_month, arrival_year = format_date(arrival_date,format="MMMM Y", locale="pt").split(" ")
    departure_month, departure_year = format_date(departure_date,format="MMMM Y", locale="pt").split(" ")
    arrival_month = arrival_month.capitalize()
    departure_month = departure_month.capitalize()

    arrival_date_elem = self.find_element(By.ID, "departure")
    self.click_on_element(arrival_date_elem)
    time.sleep(1)
    date_range_elem = self.find_element(By.CLASS_NAME, "daterangepicker")
    left_elem = date_range_elem.find_element(By.CLASS_NAME, "left")
    current_month, current_year = left_elem.find_element(By.CLASS_NAME, "month").text.split(" ")
    current_month, current_year = select_date(current_month, current_year, arrival_month, arrival_year, arrival_date.day)
    select_date(current_month, current_year, departure_month, departure_year, departure_date.day)

  def select_guests(self):

    def add_guests(quantity, element, default_value=0):
      if quantity > default_value:
        for _ in range(default_value, quantity):
          self.click_on_element(element)
          time.sleep(1)

    adult_price_age_lower_limit = 12
    baby_upper_limit = 2
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

    self.click_on_element(self.find_element(By.ID, "total_passengers"))
    guests_selector = self.find_element(By.ID, "select_passengers_body")
    add_buttons = guests_selector.find_elements(By.CLASS_NAME, "btn-add")
    add_guests(paying_adults, add_buttons[0], 1)
    add_guests(paying_minors, add_buttons[1])
    add_guests(paying_babies, add_buttons[2])
    

  def get_results(self, site_name) -> list[dict]:
    from itertools import product

    def get_info_from_container(container, prefix) -> list[dict]:
      infos = []
      info_elems = container.find_elements(By.CLASS_NAME, "select-flight-list-accordion-item")
      for info_elem in info_elems:
        info = {}
        info[f"{prefix}_company"] = info_elem.find_element(By.CLASS_NAME, "company").get_attribute("innerHTML")
        info[f"{prefix}_departure_hour"] = info_elem.find_elements(By.CLASS_NAME, "iata-code")[0].find_element(By.XPATH, "strong").text
        info[f"{prefix}_arrival_hour"] = info_elem.find_elements(By.CLASS_NAME, "iata-code")[1].find_element(By.XPATH, "strong").text
        info[f"{prefix}_flight_duration"] = info_elem.find_element(By.CLASS_NAME, "scale-duration__time").text
        info[f"{prefix}_stops"] = info_elem.find_element(By.CLASS_NAME, "scale-duration__type-flight").text
        info[f"{prefix}_miles"] = info_elem.find_element(By.CLASS_NAME, "miles").find_element(By.XPATH, "strong").text.rstrip("milhas").replace(".","")
        infos.append(info)
      return infos
    
    def blend_result(separated_result):
      result = separated_result[0] | separated_result[1]
      result["total_miles"] = str(round(int(result.pop(f"return_miles")) + int(result.pop(f"outbound_miles"))))
      result["page_url"] = self.base_url
      return result
    
    return_button_elem = self.find_element(By.ID, "select-flight-accordion-volta")
    time.sleep(5)
    self.click_on_element(return_button_elem)
    time.sleep(5)
    if len(self.driver.find_elements(By.CLASS_NAME, "select-flight-not-found-card")):
      print("No flights found for this date!")
      return []
    outbound_container_elem = self.find_element(By.CLASS_NAME, "list-ida")
    return_container_elem = self.find_element(By.CLASS_NAME, "list-volta")
    
    outbound_infos = get_info_from_container(outbound_container_elem, "outbound")
    return_infos = get_info_from_container(return_container_elem, "return")
    separated_results = product(outbound_infos, return_infos)
    
    return [blend_result(sr) for sr in separated_results]

  def scrap_website(self, url, site_name):
    self.driver.get(self.base_url)
    self.insert_cities()
    time.sleep(2)
    self.insert_dates()
    time.sleep(2)
    self.select_guests()
    time.sleep(2)
    self.click_on_element(self.find_element(By.CLASS_NAME, "checkmark"))
    self.click_on_element(self.find_element(By.CLASS_NAME, "btn-latam"))
    time.sleep(90)
    return "Foi"

    # return self.get_results(site_name)