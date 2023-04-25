from dataclasses import dataclass, field
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent

from src import DRIVER_PATH

ua = UserAgent()

@dataclass
class BaseWebScraper:
  arrival_date: str
  departure_date: str
  origin_city: str
  destiny_city: str
  guests: dict
  check_in_luggage: bool = False
  max_stops: int = -1
  delay: int = 20
  xpaths: dict = None
  guest_classes_to_value: dict = None
  driver: webdriver.Firefox = field(init=False)
  
  def __post_init__(self):
    profile = webdriver.FirefoxProfile()
    options = Options()
    user_agent = ua.random
    PROXY_HOST = "12.12.12.123"
    PROXY_PORT = "1234"
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument("--headless")
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.http", PROXY_HOST)
    options.set_preference("network.proxy.http_port", int(PROXY_PORT))
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference('useAutomationExtension', False)

    self.driver = webdriver.Firefox(executable_path=DRIVER_PATH, options=options, firefox_profile=profile)
    self.driver.set_window_size(1920, 1080)
  
  def __del__(self):
    self.driver.quit()

  def click_on_element(self, element):
    try:
      WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable(element)).click()
    except ElementClickInterceptedException:
      self.driver.execute_script("arguments[0].click();", element)

  def find_element_by_xpath(self, element_name, replace_str_new="", replace_str_old="{}"):
    return WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, self.xpaths[element_name].replace(replace_str_old, str(replace_str_new)))))

  def find_element(self, by: By, argument: str):
    return WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, argument)))

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

  def scrap_website(self):
    pass