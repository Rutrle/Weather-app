from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)

driver.get("https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324/")
# driver.get("https://techwithtim.net")
search = driver.find_element_by_id('day1')
search2 = driver.find_elements_by_css_selector('day day-ext')
print(search.text)
print('_'*10)
for element in search2:
    print(element)

time.sleep(10)
print(driver.title)
driver.quit()
