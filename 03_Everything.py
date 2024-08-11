import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/search?city=1390&locale=en-us&ckuid=d0684062-22fd-4ac1-b4f1-9eb830b8593c&prid=0&currency=USD&correlationId=a8533e34-9d23-4c69-bb92-f3bdd4c5c6d9&analyticsSessionId=4575154828477710650&pageTypeId=103&realLanguageId=1&languageId=1&origin=BD&cid=1897343&userId=d0684062-22fd-4ac1-b4f1-9eb830b8593c&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6g-acm-web-user-997bb7d77-7jhrf&trafficGroupId=4&sessionId=wlcjbtrychgwtuthkuwlar4e&trafficSubGroupId=767&aid=82172&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&cdnDomain=agoda.net&checkIn=2024-04-30&checkOut=2024-05-30&rooms=1&adults=2&children=0&priceCur=USD&los=30&textToSearch=Dhaka&travellerType=1&familyMode=off&ds=HC%2Bf7KkIdwYfqShu")

# Wait for the page to load
time.sleep(1000)

# Function to check if the next button is present
def is_next_button_present():
    try:
        driver.find_element(By.ID, "paginationNext")
        return True
    except NoSuchElementException:
        return False
# Function to extract hotel name, currency, and price
def extract_hotel_info():
    hotels = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='hotel-item']")
    for hotel in hotels:
        hotel_name = hotel.find_element(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']").text
        currency = hotel.find_element(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']").text
        price = hotel.find_element(By.CSS_SELECTOR, "span[data-selenium='display-price']").text
        print(hotel_name, currency, price)

# Find all hotel names, currencies, and prices on the first page
extract_hotel_info()

# Pagination - locate and click on the next page button if available
while is_next_button_present():
    next_button = driver.find_element(By.ID, "paginationNext")
    driver.execute_script("arguments[0].click();", next_button)  # Click using JavaScript
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='hotel-item']")))
    extract_hotel_info()

driver.quit()
