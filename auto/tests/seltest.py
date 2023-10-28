from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

display = Display(visible=0, size=(800, 600))
display.start()
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = uc.Chrome(options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

# Navigate to a website
driver.get("https://www.apkmirror.com/apk/red-apps-ltd/sync-for-reddit/")

# Find an element by its CSS selector and interact with it
element = driver.find_element(By.CSS_SELECTOR, "h1")
print(element.text)

# Close the browser
driver.quit()
display.stop()
