#%%
import time
import os
from unidecode import unidecode
from datetime import datetime
from dataclasses import dataclass, field
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# from src import DRIVER_PATH
DRIVER_PATH = '../drivers/geckodriver'
#%%
@dataclass
class BaseWebScraper:
  urls: dict
  arrival_date: str
  departure_date: str
  origin_city: str
  destiny_city: str
  guests: dict
  check_in_luggage: bool
  max_stops: int = -1
  delay: int = 20
  xpaths: dict = None
  guest_classes_to_value: dict = None
  drive: webdriver.Firefox = field(init=False)
  
  def __post_init__(self):
    self.driver = webdriver.Firefox(executable_path=DRIVER_PATH)

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
#%%
class DecolarWebScraper(BaseWebScraper):
  xpaths = {
    "close_login_popup": "/html/body/div[8]/div/nav/div[6]/div[1]/i",
    "filter_max_stops": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[1]/div[1]/span/filters/div/div/ul/filter-group[1]/li/ul/div/checkbox-filter/checkbox-filter-item[{}]/li/span/span[1]/span/label/i",
    "filter_check_in_luggage": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[1]/div[1]/span/filters/div/div/ul/filter-group[2]/li/ul/div/checkbox-filter/checkbox-filter-item[3]/li/span/span[1]/span/label/i",
    "results_price_by_adult": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/main-fare/span/span[2]/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_price_without_taxes": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/fare-details-items/div/span/item-fare[1]/p/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_price_taxes": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/fare-details-items/div/span/item-fare[2]/p/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_price_total": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[2]/fare/span/span/fare-details-items/div/item-fare/p/span/flights-price/span/flights-price-element/span/span/em/span[2]",
    "results_outbound_company": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span/span/span/span/span[2]/span",
    "results_outbound_departure_hour": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[1]/span/span/span",
    "results_outbound_arrival_hour": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[1]/span/span/span/span",
    "results_outbound_stops": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[2]/span/stops-count-item/span/span/span[1]",
    "results_outbound_flight_duration": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[1]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[2]/span/duration-item/span/span",
    "results_return_company": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[1]/itinerary-element[2]/span/itinerary-element-airline/span/span/span/span/span[2]/span",
    "results_return_departure_hour": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[1]/span/span/span",
    "results_return_arrival_hour": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[1]/span/span/span/span",
    "results_return_stops": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[2]/itinerary-element[2]/span/stops-count-item/span/span/span[1]",
    "results_return_flight_duration": "/html/body/div[10]/div[4]/div/div/div[3]/div/div[2]/div/div[4]/app-root/app-common/items/div/span[1]/div/span/cluster/div/div/div[1]/div/span/div/div/span[2]/route-choice/ul/li{}/route/itinerary/div/div/div[3]/itinerary-element[2]/span/duration-item/span/span",
  }
  guest_classes_to_value = {
    "economy": "YC",
    "premium_economy": "PE",
    "business": "C",
    "first_class": "F",
  }

  def __init__(self, **kwargs):
    super().__init__(**kwargs, guest_classes_to_value=self.guest_classes_to_value, xpaths=self.xpaths)
    self.base_url = "https://www.decolar.com/shop/flights/results/roundtrip/"
  
  def insert_cities(self):
    codes_df = pd.read_csv("./ip2location-iata-icao-master/iata-icao.csv")

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
      checkbox_position = str(2+self.max_stops)
      filter_max_stops_elem = self.find_element('filter_max_stops', checkbox_position)
      self.click_on_element(filter_max_stops_elem)
      time.sleep(2)
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
    self.insert_cities()
    self.insert_dates()
    self.select_guests()
    self.driver.get(self.base_url)
    try:
      close_login_popup_elem = self.find_element('close_login_popup')
      self.click_on_element(close_login_popup_elem)
    except TimeoutException:
      print("Login popup did not show.")
    self.apply_filters()

    return self.get_results(site_name)
#%%
class GoogleNotCurrentYearException(Exception):
  pass

class GoogleMaxStopsFilterException(Exception):
  pass

class GoogleFlightsWebScraper(BaseWebScraper):
  xpaths = {
    "origin_city_click": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input",
    "destiny_city_click": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input",
    "origin_city": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input",
    "destiny_city": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input",
    "arrival_date": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input",
    "box_date_apply": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button",
    "departure_date": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div/input",
    "guests": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[1]/div/button",
    "guests_adults_increase_button": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/ul/li[1]/div/div/span[3]/button",
    "guests_minors_0_to_2_increase_button": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/ul/li[4]/div/div/span[3]/button",
    "guests_minors_2_to_11_increase_button": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/ul/li[2]/div/div/span[3]/button",
    "guests_minors_11_to_18_increase_button": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/ul/li[3]/div/div/span[3]/button",
    "guests_apply": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div/div[2]/div[2]/button[1]",
    "guests_class_button": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]/div/div[1]/div[1]/div/button",
    "guests_class_selection": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]/div/div[1]/div[2]/div[2]/ul/li[{}]",
    "search": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button",
    "filter_max_stops_button": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div/div[2]/div[1]/div/div[1]/span/button",
    "filter_max_stops_0": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div[3]/div/div[1]/section/div[2]/div[1]/div/div/div[2]/label",
    "filter_max_stops_1": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div[3]/div/div[1]/section/div[2]/div[1]/div/div/div[3]/label",
    "filter_max_stops_2": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[4]/div/div[2]/div[3]/div/div[1]/section/div[2]/div[1]/div/div/div[4]/label",
    # "results_price_by_adult": "",
    # "results_price_without_taxes": "",
    # "results_price_taxes": "",
    # "results_price_total": "",
    # "results_outbound_company": "",
    # "results_outbound_departure_hour": "",
    # "results_outbound_arrival_hour": "",
    # "results_outbound_stops": "",
    # "results_outbound_flight_duration": "",
    # "results_return_company": "",
    # "results_return_departure_hour": "",
    # "results_return_arrival_hour": "",
    # "results_return_stops": "",
    # "results_return_flight_duration": "",
  }

  guest_classes_to_value = {
    "economy": "1",
    "premium_economy": "2",
    "business": "3",
    "first_class": "4",
  }
  
  def __init__(self, **kwargs):
    super().__init__(**kwargs, guest_classes_to_value=self.guest_classes_to_value, xpaths=self.xpaths)
  
  def insert_cities(self):
    origin_city_click_elem = self.find_element('origin_city_click')
    self.click_on_element(origin_city_click_elem)
    origin_city_elem = self.find_element('origin_city')
    origin_city_elem.send_keys(Keys.END)
    time.sleep(0.5)
    origin_city_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(50)]))
    time.sleep(1)
    origin_city_elem.send_keys(self.origin_city)
    time.sleep(1)
    origin_city_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    destiny_city_click_elem = self.find_element('destiny_city_click')
    self.click_on_element(destiny_city_click_elem)
    destiny_city_elem = self.find_element('destiny_city')
    destiny_city_elem.send_keys(self.destiny_city)
    time.sleep(1)
    destiny_city_elem.send_keys(Keys.RETURN)
    time.sleep(1)

  def insert_dates(self):
    from babel.dates import format_date
    from datetime import date
    today = date.today()

    arrival_date = date.fromisoformat(self.arrival_date)
    departure_date = date.fromisoformat(self.departure_date)
    if arrival_date.year != today.year or departure_date.year != today.year:
      raise GoogleNotCurrentYearException

    arrival_date_input = format_date(arrival_date, format='E, d {} MMM', locale='pt').format("de")
    departure_date_input = format_date(departure_date, format='E, d {} MMM', locale='pt').format("de")
    
    arrival_date_elem = self.find_element('arrival_date')
    self.click_on_element(arrival_date_elem)
    arrival_date_elem.send_keys(Keys.END)
    time.sleep(0.5)
    arrival_date_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(10)]))
    time.sleep(1)
    arrival_date_elem.send_keys(arrival_date_input)
    time.sleep(1)
    arrival_date_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    departure_date_elem = self.find_element('departure_date')
    self.click_on_element(departure_date_elem)
    departure_date_elem.send_keys(Keys.END)
    time.sleep(0.5)
    departure_date_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(10)]))
    time.sleep(1)
    departure_date_elem.send_keys(departure_date_input)
    time.sleep(1)
    departure_date_elem.send_keys(Keys.RETURN)
    time.sleep(1)

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
      for age in self.guests['minors']['ages']:
        if age < 0:
          raise ValueError("Invalid age: {}".format(age))
        elif age < 2:
          guests_increase_minors_button_elem = self.find_element('guests_minors_0_to_2_increase_button')
        elif age <= 11:
          guests_increase_minors_button_elem = self.find_element('guests_minors_2_to_11_increase_button')
        elif age <= 18:
          guests_increase_minors_button_elem = self.find_element('guests_minors_11_to_18_increase_button')
        else:
          raise ValueError("Invalid age: {}".format(age))
        self.click_on_element(guests_increase_minors_button_elem)
    self.click_on_element(self.find_element('guests_apply'))

    guests_class_button_elem = self.find_element('guests_class_button')
    self.click_on_element(guests_class_button_elem)

    guests_class_selection_elem = self.find_element('guests_class_selection', self.guest_classes_to_value[self.guests['class']])
    self.click_on_element(guests_class_selection_elem)
    
  def apply_filters(self):
    filter_max_stops_button_elem = self.find_element("filter_max_stops_button")

    if self.max_stops != -1:
      self.click_on_element(filter_max_stops_button_elem)
      try:
        if self.max_stops == 0:
          filter_max_stops_radio_elem = self.find_element("filter_max_stops_0")
        elif self.max_stops == 1:
          filter_max_stops_radio_elem = self.find_element("filter_max_stops_1")
        elif self.max_stops == 2:
          filter_max_stops_radio_elem = self.find_element("filter_max_stops_2")
        self.click_on_element(filter_max_stops_radio_elem)
      except TimeoutException:
        raise GoogleMaxStopsFilterException()

  def get_results(self, site_name):
    return {
      "site_name": site_name
    }

  def scrap_website(self, url, site_name):
    self.driver.get(url)
    self.insert_cities()
    self.select_guests()
    self.insert_dates()
    try:
      self.click_on_element(self.find_element('search'))
    except (TimeoutException, StaleElementReferenceException):
      pass
    self.apply_filters()

    return self.get_results(site_name)

site_to_ws_class = {
  "decolar": DecolarWebScraper,
  "google_flights": GoogleFlightsWebScraper
}

def scraping_entrypoint(**kwargs):
  results = []
  for site_name, url in kwargs["urls"].items():
    ws = site_to_ws_class[site_name](**kwargs)
    results.append(ws.scrap_website(url, site_name))
  return results

#%%
kwargs = {
  "urls": {
    "decolar": "https://decolar.com/passagens-aereas/"
    # "google_flights": "https://www.google.com/flights?hl=pt-BR"
  },
  
  "arrival_date": "2023-05-20",
  "departure_date": "2023-05-25",
  "origin_city": "SAO",
  "destiny_city": "RIO",
  "guests": {
    "adults": 2,
    "minors": {
      "amount": 1,
      "ages": [15]
    },
    "class": "economy"
  },
  "check_in_luggage": True,
  "max_stops": 0
}
#%%
ws = DecolarWebScraper(**kwargs)
print(ws.scrap_website("https://decolar.com/passagens-aereas", "decolar"))
ws.driver.quit()

# ws = GoogleFlightsWebScraper(**kwargs)
# ws.scrap_website("https://www.google.com/flights?hl=pt-BR", "google_flights")
#%%
response = scraping_entrypoint(**kwargs)
# %%
