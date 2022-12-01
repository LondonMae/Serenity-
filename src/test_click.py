from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
# Go to your page url
driver.get('http://localhost:8888/#access_token=BQCuOuttg648JGBVheGTALkD5Wpj2lcQ49Cv4vvTTXMLnMG9q9bfRP4-W0yuCy9TFWHZfeaFzX7lVOQjWaf5nxkbrhbUFLyYzWC8M3_k59Cg1KAjY4AYo8XLl4oRBBPNXyXMfFRR2bDvxk0iJie2oU7Jube7vd3B4w0cMvrxBzDgq8hQYTCBYYmWZ70ZYi-nBHzvVkOVVMF8Kb1O&refresh_token=AQAtOO6HdKWiZ7hoRdl3WACwqwwrQqpucIj7YR5B_oPT7Z2toi-1jcwGXo4ff9P0wmUb841VN4cqGQcbagEh8e5Hnd5byBNfsGv9M-Kt407zqtJtGmU4t_AzZTkjaURdqYQ')
# Get button you are going to click by its id ( also you could us find_element_by_css_selector to get element by css selector)
button_element = driver.find_element(By.ID, 'togglePlay')
button_element.click()

time.sleep(10)
