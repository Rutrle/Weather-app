from selenium import webdriver
path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(executable_path=path)
driver.get("https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324/")
print(driver.title)
driver.quit()


