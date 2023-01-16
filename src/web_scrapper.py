#%%
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC

# from src import DRIVER_PATH
DRIVER_PATH = '../drivers/geckodriver'
#%%
class WebScrapper:

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
    "search": "/html/body/div[7]/div[1]/div/div/div/div/div/div/div[3]/div[3]/button"
  }

  guest_classes_to_value = {
    "economy": "YC",
    "premium_economy": "PE",
    "business": "C",
    "first_class": "F",
  }

  delay = 20
  
  def __init__(self, urls: dict, arrival_date: str, departure_date: str, origin_city: str, destiny_city: str, guests: int):
    self.driver = webdriver.Firefox(executable_path=DRIVER_PATH)
    self.urls = urls
    self.arrival_date = arrival_date
    self.departure_date = departure_date
    self.origin_city = origin_city
    self.destiny_city = destiny_city
    self.guests = guests
    
  def __del__(self):
    self.driver.quit()

  def click_on_element(self, element):
    try:
      WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable(element)).click()
    except ElementClickInterceptedException:
      self.driver.execute_script("arguments[0].click();", element)

  def find_element(self, element_name, replace_str_old="{}", replace_str_new=""): 
    if not replace_str_new:
      return WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, self.xpaths[element_name])))
    return WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, self.xpaths[element_name].replace(replace_str_old, str(replace_str_new)))))

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
    
  def scrap_website(self, url):
    self.driver.get(url)
    self.insert_cities()
    self.insert_dates()
    self.select_guests()
    search_elem = self.find_element('search')
    self.click_on_element(search_elem)

    return 1

  def scrap_urls(self):
    results = {}
    for site_name, url in self.urls.items():
      results[site_name] = self.scrap_website(url)
    return results
# %%
args = {
  "urls": {
    "decolar": "https://decolar.com"
  },
  
  "arrival_date": "2023-03-20",
  "departure_date": "2023-03-30",
  "origin_city": "Rio de Janeiro",
  "destiny_city": "Orlando",
  "guests": {
    "adults": 2,
    "minors": {
      "amount": 1,
      "ages": [15]
    },
    "class": "business"
  }
}

# %%
ws = WebScrapper(**args)
ws.scrap_urls()
# %%
del ws