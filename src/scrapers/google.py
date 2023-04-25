import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from src.scrapers.base import BaseWebScraper

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
    "results_ul": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul",
    "return_to_outbound": "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[2]/div/ol/li[1]/span/span/span/div/div"
  }

  guest_classes_to_value = {
    "economy": "1",
    "premium_economy": "2",
    "business": "3",
    "first_class": "4",
  }
  
  def __init__(self, **kwargs):
    super().__init__(**kwargs, guest_classes_to_value=self.guest_classes_to_value, xpaths=self.xpaths)
    self.base_url = "https://www.google.com/flights?hl=pt-BR"
  
  def insert_cities(self):
    origin_city_click_elem = self.find_element_by_xpath('origin_city_click')
    self.click_on_element(origin_city_click_elem)
    origin_city_elem = self.find_element_by_xpath('origin_city')
    origin_city_elem.send_keys(Keys.END)
    time.sleep(0.5)
    origin_city_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(50)]))
    time.sleep(1)
    origin_city_elem.send_keys(self.origin_city)
    time.sleep(1)
    origin_city_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    destiny_city_click_elem = self.find_element_by_xpath('destiny_city_click')
    self.click_on_element(destiny_city_click_elem)
    destiny_city_elem = self.find_element_by_xpath('destiny_city')
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
    
    arrival_date_elem = self.find_element_by_xpath('arrival_date')
    self.click_on_element(arrival_date_elem)
    arrival_date_elem.send_keys(Keys.END)
    time.sleep(0.5)
    arrival_date_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(10)]))
    time.sleep(1)
    arrival_date_elem.send_keys(arrival_date_input)
    time.sleep(1)
    arrival_date_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    departure_date_elem = self.find_element_by_xpath('departure_date')
    self.click_on_element(departure_date_elem)
    departure_date_elem.send_keys(Keys.END)
    time.sleep(0.5)
    departure_date_elem.send_keys("".join([Keys.BACK_SPACE for _ in range(10)]))
    time.sleep(1)
    departure_date_elem.send_keys(departure_date_input)
    time.sleep(1)
    departure_date_elem.send_keys(Keys.RETURN)
    time.sleep(1)

    box_date_apply_elem = self.find_element_by_xpath('box_date_apply')
    self.click_on_element(box_date_apply_elem)

  def select_guests(self):
    guests_elem = self.find_element_by_xpath('guests')
    self.click_on_element(guests_elem)
    if self.guests['adults'] > 1:
      guests_adults_increase_button_elem = self.find_element_by_xpath('guests_adults_increase_button')
      for _ in range(self.guests['adults'] - 1):
        self.click_on_element(guests_adults_increase_button_elem)
    if self.guests['minors']['amount'] > 0:
      for age in self.guests['minors']['ages']:
        if age < 0:
          raise ValueError("Invalid age: {}".format(age))
        elif age < 2:
          guests_increase_minors_button_elem = self.find_element_by_xpath('guests_minors_0_to_2_increase_button')
        elif age <= 11:
          guests_increase_minors_button_elem = self.find_element_by_xpath('guests_minors_2_to_11_increase_button')
        elif age <= 18:
          guests_increase_minors_button_elem = self.find_element_by_xpath('guests_minors_11_to_18_increase_button')
        else:
          raise ValueError("Invalid age: {}".format(age))
        self.click_on_element(guests_increase_minors_button_elem)
    self.click_on_element(self.find_element_by_xpath('guests_apply'))

    guests_class_button_elem = self.find_element_by_xpath('guests_class_button')
    self.click_on_element(guests_class_button_elem)

    guests_class_selection_elem = self.find_element_by_xpath('guests_class_selection', self.guest_classes_to_value[self.guests['class']])
    self.click_on_element(guests_class_selection_elem)
    
  def apply_filters(self):
    filter_max_stops_button_elem = self.find_element_by_xpath("filter_max_stops_button")

    if self.max_stops != -1:
      self.click_on_element(filter_max_stops_button_elem)
      try:
        if self.max_stops == 0:
          filter_max_stops_radio_elem = self.find_element_by_xpath("filter_max_stops_0")
        elif self.max_stops == 1:
          filter_max_stops_radio_elem = self.find_element_by_xpath("filter_max_stops_1")
        elif self.max_stops == 2:
          filter_max_stops_radio_elem = self.find_element_by_xpath("filter_max_stops_2")
        self.click_on_element(filter_max_stops_radio_elem)
      except TimeoutException:
        raise GoogleMaxStopsFilterException()

  def get_results(self):
    results_list= []
    max_results = 10
    time.sleep(5)
    for i in range(max_results):

      results_ul_outbound_elem = self.find_element_by_xpath("results_ul")
      try:
        outbound_result_elem = results_ul_outbound_elem.find_elements(By.XPATH, "li")[i+1]
      except IndexError:
        break

      results = {}
      outbound_price = outbound_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[6]/div[1]/div[2]/span").text.lstrip("R$").replace(".", "")
      results["outbound_company"] = " ".join([elem.text for elem in outbound_result_elem.find_elements(By.XPATH, "div/div[2]/div/div[2]/div[2]/div[2]/span")])
      results["outbound_departure_hour"] = outbound_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[2]/div[1]/span/span[1]/span/span/span").text
      results["outbound_arrival_hour"] = outbound_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[2]/div[1]/span/span[2]/span/span/span").text.split("+")[0]
      results["outbound_flight_duration"] = outbound_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[3]/div").text
      results["outbound_stops"] = outbound_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[4]/div[1]/span").text
      
      self.click_on_element(outbound_result_elem)
      time.sleep(2)

      results_ul_return_elem = self.find_element_by_xpath("results_ul")
      return_result_elem = results_ul_return_elem.find_elements(By.XPATH, "li")[0]

      return_price = return_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[6]/div[1]/div[2]/span").text.lstrip("R$").replace(".", "")
      results["return_company"] = " ".join([elem.text for elem in return_result_elem.find_elements(By.XPATH, "div/div[2]/div/div[2]/div[2]/div[2]/span")])
      results["return_departure_hour"] = return_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[2]/div[1]/span/span[1]/span/span/span").text
      results["return_arrival_hour"] = return_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[2]/div[1]/span/span[2]/span/span/span").text.split("+")[0]
      results["return_flight_duration"] = return_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[3]/div").text
      results["return_stops"] = return_result_elem.find_element(By.XPATH, "div/div[2]/div/div[2]/div[4]/div[1]/span").text

      results["total_price"] = str(int(outbound_price) + int(return_price))
      results["page_url"] = self.driver.current_url
      results_list.append(results)

      return_to_outbound_elem = self.find_element_by_xpath("return_to_outbound")
      self.click_on_element(return_to_outbound_elem)
      time.sleep(2)

    return results_list

  def scrap_website(self):
    self.driver.get(self.base_url)
    self.insert_cities()
    self.select_guests()
    self.insert_dates()
    try:
      self.click_on_element(self.find_element_by_xpath('search'))
    except (TimeoutException, StaleElementReferenceException):
      pass
    print(self.driver.current_url)

    return self.get_results()
