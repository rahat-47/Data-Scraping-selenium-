import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/search?city=1390&locale=en-us&ckuid=d0684062-22fd-4ac1-b4f1-9eb830b8593c&prid=0&currency=USD&correlationId=5873e7e6-3e22-4487-9fd2-02c717f36bd0&analyticsSessionId=4575154828477710650&pageTypeId=103&realLanguageId=1&languageId=1&origin=BD&cid=1897343&userId=d0684062-22fd-4ac1-b4f1-9eb830b8593c&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6g-acm-web-user-997bb7d77-ss7fn&trafficGroupId=4&sessionId=wlcjbtrychgwtuthkuwlar4e&trafficSubGroupId=767&aid=82172&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&cdnDomain=agoda.net&checkIn=2024-04-25&checkOut=2024-04-30&rooms=1&adults=2&children=0&priceCur=USD&los=5&textToSearch=Dhaka&productType=-1&travellerType=1&familyMode=off&ds=HC%2Bf7KkIdwYfqShu")
# Wait for the page to load
time.sleep(10)

# Function to check if the next button is present
def is_next_button_present():
    try:
        driver.find_element(By.ID, "paginationNext")
        return True
    except NoSuchElementException:
        return False

# Find all hotel names, currencies, and prices on the first page
hotel_names = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")))
hotel_currencies = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")))
hotel_prices = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='display-price']")))
#hotel_properties = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='pill-container']")))

while True:
    # Scroll down to the last elements in the lists
    driver.execute_script('arguments[0].scrollIntoView();', hotel_names[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_currencies[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_prices[-1])
    #driver.execute_script('arguments[0].scrollIntoView();', hotel_properties[-1])
    try:
        # Wait for more elements to be loaded
        wait(driver, 15).until(lambda driver: len(wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")))) > len(hotel_names))
        wait(driver, 15).until(lambda driver: len(wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")))) > len(hotel_currencies))
        wait(driver, 15).until(lambda driver: len(wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='display-price']")))) > len(hotel_prices))
        #wait(driver, 15).until(lambda driver: len(wait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='pill-container']")))) > len(hotel_properties))
        # Update lists
        hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
        hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
        hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
        #hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
        
    except:
        # Break the loop if no new elements are loaded after scrolling
        break

# Write data to CSV
with open('dhaka_hotel.csv', 'w') as f:
    for hotel_name, hotel_currency, display_price in zip(hotel_names, hotel_currencies, hotel_prices ):
        line = f"{hotel_name.text},{hotel_currency.text},{display_price.text}\n"
        f.write(line)

# Pagination - locate and click on the next page button if available
while is_next_button_present():
    next_button = driver.find_element(By.ID, "paginationNext")
    driver.execute_script("arguments[0].click();", next_button)  # Click using JavaScript
    time.sleep(10)  # Let the new page load
    
    # Refresh elements
    hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
    hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
    hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
    #hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
    while True:
        # Scroll down to last elements in lists
        driver.execute_script('arguments[0].scrollIntoView();', hotel_names[-1])
        driver.execute_script('arguments[0].scrollIntoView();', hotel_currencies[-1])
        driver.execute_script('arguments[0].scrollIntoView();', hotel_prices[-1])
        #driver.execute_script('arguments[0].scrollIntoView();', hotel_properties[-1])
        try:
            # Wait for more elements to be loaded
            wait(driver, 15).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")) > len(hotel_names))
            wait(driver, 15).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")) > len(hotel_currencies))
            wait(driver, 15).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")) > len(hotel_prices))
            #wait(driver, 15).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR,  "div[data-selenium='pill-container']")) > len(hotel_properties))
            # Update lists
            hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
            hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
            hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
           # hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
        except:
            # Break the loop if no new elements are loaded after scrolling
            break

driver.quit()
