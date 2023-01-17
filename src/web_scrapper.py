#%%
import time
from datetime import datetime
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from src import DRIVER_PATH
# DRIVER_PATH = '../drivers/geckodriver'
#%%
@dataclass
class BaseWebScrapper:
  urls: dict
  arrival_date: str
  departure_date: str
  origin_city: str
  destiny_city: str
  guests: dict
  check_in_luggage: bool
  one_stop: bool
  delay: int = 20
  xpaths: dict = None
  guest_classes_to_value: dict = None
  driver = webdriver.Firefox(executable_path=DRIVER_PATH)

  def __del__(self):
    self.driver.quit()

  def click_on_element(self, element):
    try:
      WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable(element)).click()
    except ElementClickInterceptedException:
      self.driver.execute_script("arguments[0].click();", element)

  def find_element(self, element_name, replace_str_new="", replace_str_old="{}"):
    return WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, self.xpaths[element_name].replace(replace_str_old, str(replace_str_new)))))

  def insert_cities(self):
    pass

  def insert_dates(self):
    pass

  def select_guests(self):
    pass

  def apply_filters(self):
    pass

  def get_results(self):
    pass

  def scrap_website(self, url, site_name):
    pass

class DecolarWebScrapper(BaseWebScrapper):
  xpaths = {
    "origin_city": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/input",
    "destiny_city": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div/input",
    "arrival_date": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/input",
    "departure_date": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div/input",
    "guests": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[1]/div[1]/div[4]/div/div/div/div/input",
    "guests_adults_increase_button": "/html/body/div[9]/div[3]/div/div/div[1]/div[1]/div[2]/div/button[2]",
    "guests_minors_increase_button": "/html/body/div[9]/div[3]/div/div/div[1]/div[2]/div[2]/div/button[2]",
    "guests_minors_age_selector": "/html/body/div[9]/div[3]/div/div/div[1]/div[{}]/div[2]/div/div/select",
    "guests_class_selector": "/html/body/div[9]/div[3]/div/div/div[2]/div[2]/div/div/div/select",
    "guests_apply": "/html/body/div[9]/div[3]/div/div/div[3]/a",
    "current_month": "/html/body/div[9]/div[1]/div[1]/div[2]/div[1]",
    "box_date_day": "/html/body/div[9]/div[1]/div[1]/div[2]/div[1]/div[3]/div[{}]/div",
    "box_date_right_arrow": "/html/body/div[9]/div[1]/div[1]/div[2]/a[2]",
    "box_date_apply": "/html/body/div[9]/div[1]/div[2]/div/button",
    "search": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[3]/button",
    "close_login_popup": "/html/body/div[10]/div/nav/div[6]/div[1]/i",
    "filter_one_stop": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[1]/div[1]/span/filters/div/div/ul/filter-group[1]/li/ul/div/checkbox-filter/checkbox-filter-item[2]/li/span/span[1]/span/label/i",
    "filter_check_in_luggage": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[1]/div[1]/span/filters/div/div/ul/filter-group[2]/li/ul/div/checkbox-filter/checkbox-filter-item[3]/li/span/span[1]/span/label/i",
    "results_price_by_adult": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/main-fare/span/span[2]/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_price_without_taxes": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/fare-details-items/div/span/item-fare[1]/p/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_price_taxes": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/fare-details-items/div/span/item-fare[2]/p/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_price_total": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/fare-details-items/div/item-fare/p/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_outbound_company": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span/span/span/span/span[2]/span",
    "results_outbound_departure_hour": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[1]/span/span/span",
    "results_outbound_arrival_hour": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[1]/span/span/span/span",
    "results_outbound_stops": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[2]/span/stops-count-item/span/span/span[1]",
    "results_outbound_flight_duration": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[2]/span/duration-item/span/span",
    "results_return_company": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span/span/span/span/span[2]/span",
    "results_return_departure_hour": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[1]/span/span/span",
    "results_return_arrival_hour": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[1]/span/span/span/span",
    "results_return_stops": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[2]/span/stops-count-item/span/span/span[1]",
    "results_return_flight_duration": "/html/body/div[13]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[2]/span/duration-item/span/span",
  }
  guest_classes_to_value = {
    "economy": "YC",
    "premium_economy": "PE",
    "business": "C",
    "first_class": "F",
  }
  delay = 20

  def __init__(self, **kwargs):
    super().__init__(**kwargs, delay=self.delay, guest_classes_to_value=self.guest_classes_to_value, xpaths=self.xpaths)
  
  def insert_cities(self):
    origin_city_elem = self.find_element('origin_city')
    self.click_on_element(origin_city_elem)
    origin_city_elem.send_keys(Keys.END)
    time.sleep(0.5)
    origin_city_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(len("Sao Paulo, Brasil"))]))
    time.sleep(1)
    origin_city_elem.send_keys(self.origin_city)
    time.sleep(1)
    origin_city_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    destiny_city_elem = self.find_element('destiny_city')
    self.click_on_element(destiny_city_elem)
    destiny_city_elem.send_keys(self.destiny_city)
    time.sleep(1)
    destiny_city_elem.send_keys(Keys.RETURN)
    time.sleep(1)

  def insert_dates(self):
    arrival_date_elem = self.find_element('arrival_date')
    self.click_on_element(arrival_date_elem)
    
    current_month_elem = self.find_element('current_month')
    box_date_right_arrow_elem = self.find_element('box_date_right_arrow')
    curr_date = datetime.fromisoformat(current_month_elem.get_attribute("data-month") + "-01")

    arrival_date = datetime.fromisoformat(self.arrival_date)
    while curr_date.year < arrival_date.year or curr_date.month < arrival_date.month:
      self.click_on_element(box_date_right_arrow_elem)
      curr_date = datetime.fromisoformat(current_month_elem.get_attribute("data-month") + "-01")
    arrival_date_day_elem = self.find_element('box_date_day', replace_str_new=arrival_date.day)
    self.click_on_element(arrival_date_day_elem)

    departure_date = datetime.fromisoformat(self.departure_date)
    while curr_date.year < departure_date.year or curr_date.month < departure_date.month:
      self.click_on_element(box_date_right_arrow_elem)
      curr_date = datetime.fromisoformat(current_month_elem.get_attribute("data-month") + "-01")
    departure_date_day_elem = self.find_element('box_date_day', replace_str_new=departure_date.day)
    self.click_on_element(departure_date_day_elem)

    box_date_apply_elem = self.find_element('box_date_apply')
    self.click_on_element(box_date_apply_elem)

  def select_guests(self):
    guests_elem = self.find_element('guests')
    self.click_on_element(guests_elem)
    if self.guests['adults'] > 1:
      guests_adults_increase_button_elem = self.find_element('guests_adults_increase_button')
      for _ in range(self.guests['adults'] - 1):
        self.click_on_element(guests_adults_increase_button_elem)
    if self.guests['minors']['amount'] > 0:
      guests_minors_increase_button_elem = self.find_element('guests_minors_increase_button')
      for i in range(self.guests['minors']['amount']):
        self.click_on_element(guests_minors_increase_button_elem)
        guests_minors_age_selector_elem = self.find_element('guests_minors_age_selector', replace_str_new=3+i)
        selector = Select(guests_minors_age_selector_elem)
        selector.select_by_value(str(self.guests['minors']['ages'][0]))
    guests_class_selector_elem = self.find_element('guests_class_selector')
    selector = Select(guests_class_selector_elem)
    selector.select_by_value(self.guest_classes_to_value[self.guests['class']])

    self.click_on_element(self.find_element('guests_apply'))

  def apply_filters(self):
    filter_one_stop_elem = self.find_element('filter_one_stop')
    self.click_on_element(filter_one_stop_elem)
    filter_check_in_luggage_elem = self.find_element('filter_check_in_luggage')
    self.click_on_element(filter_check_in_luggage_elem)
    time.sleep(2)

  def get_results(self, site_name) -> dict:
    return {
      "price_by_adult": self.find_element('results_price_by_adult').text,
      "price_without_taxes": self.find_element('results_price_without_taxes').text,
      "price_taxes": self.find_element('results_price_taxes').text,
      "price_total": self.find_element('results_price_total').text,
      "outbound_company": self.find_element('results_outbound_company').text,
      "outbound_departure_hour": self.find_element('results_outbound_departure_hour').text,
      "outbound_arrival_hour": self.find_element('results_outbound_arrival_hour').text,
      "outbound_stops": self.find_element('results_outbound_stops').text,
      "outbound_flight_duration": self.find_element('results_outbound_flight_duration').text,
      "return_company": self.find_element('results_return_company').text,
      "return_departure_hour": self.find_element('results_return_departure_hour').text,
      "return_arrival_hour": self.find_element('results_return_arrival_hour').text,
      "return_stops": self.find_element('results_return_stops').text,
      "return_flight_duration": self.find_element('results_return_flight_duration').text,
      "site_name": site_name,
      "page_url": self.driver.current_url,
    }

  def scrap_website(self, url, site_name):
    self.driver.get(url)
    self.insert_cities()
    self.insert_dates()
    self.select_guests()
    search_elem = self.find_element('search')
    self.click_on_element(search_elem)
    try:
      close_login_popup_elem = self.find_element('close_login_popup')
      self.click_on_element(close_login_popup_elem)
    except TimeoutException:
      print("Login popup did not show.")
    self.apply_filters()

    return self.get_results(site_name)

site_to_ws_class = {
  "decolar": DecolarWebScrapper
}

def scrapping_entrypoint(**kwargs):
  results = []
  for site_name, url in kwargs["urls"].items():
    ws = site_to_ws_class[site_name](**kwargs)
    results.append(ws.scrap_website(url, site_name))
  return results