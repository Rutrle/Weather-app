from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)

# driver.get("https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324/")
driver.get("https://techwithtim.net")
search = driver.find_element_by_name("s")
print(driver.page_source)
search.send_keys("test")
search.send_keys(Keys.RETURN)
# find things and then close page
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)


finally:
    driver.quit()
