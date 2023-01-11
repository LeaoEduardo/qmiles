#%%

from selenium import webdriver

from src import DRIVER_PATH
# DRIVER_PATH = '../drivers/geckodriver'

#%%
class WebScrapper:
  
  def __init__(self):
    self.browser = webdriver.Firefox(executable_path=DRIVER_PATH)

  def __del__(self):
    self.browser.quit()
# %%

