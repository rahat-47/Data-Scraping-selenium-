import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/search?guid=a636d8b1-1ed1-491b-abff-4ef52841a6bd&hotel=37840737&selectedproperty=37840737&asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9v1t%2B%2FBvi2S2XFkL6ePY8Z8jH%2BC610XsB%2B2%2BxvxkhHjMYfVmtZbDxpuNOKKwN98ANTuDhkY79Irw0TtjfUkGqqK%2BkA7OPAuoToy87mFL5RIDpvt0GnK0DA1BOyZCQH87tZd25qt2zaGe4ZrztUCrefF1SKUwvkpne9D90HIWG9PiPyk5mR%2FpbD3ck8HPXYe9P9JpyKpc0u561TnnTz5xm1GnbDbaTUZoenSwwmLQltqQ%3D&tick=638508170874&locale=en-us&ckuid=1b523278-4aef-4484-9db1-0e967dbaf66f&prid=0&currency=USD&correlationId=df9819be-5576-407e-be0b-2fcaaaf0b888&analyticsSessionId=9039097090895341356&pageTypeId=1&realLanguageId=1&languageId=1&origin=BD&stateCode=13&cid=-1&userId=1b523278-4aef-4484-9db1-0e967dbaf66f&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6f-acm-web-user-7cc5f9979c-5dz7x&trafficGroupId=4&sessionId=30c4tf42gn2vxaysmbqqfgft&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Edge+%28Chromium%29+for+Windows&cdnDomain=agoda.net&checkIn=2024-05-14&checkOut=2024-05-21&rooms=1&adults=2&children=0&priceCur=USD&los=7&textToSearch=Jashore+IT+Park+Hotel+and+Resort&travellerType=1&familyMode=off&ds=TxONpzFq2K3JnOyw&productType=-1")
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
hotel_names = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")))
hotel_currencies = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")))
hotel_prices = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='display-price']")))
hotel_properties = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='pill-container']")))

while True:
    # Scroll down to the last elements in the lists
    driver.execute_script('arguments[0].scrollIntoView();', hotel_names[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_currencies[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_prices[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_properties[-1])
    try:
        # Wait for more elements to be loaded
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")))) > len(hotel_names))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")))) > len(hotel_currencies))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='display-price']")))) > len(hotel_prices))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='pill-container']")))) > len(hotel_properties))
        
        # Update lists
        hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
        if not hotel_names:
            continue  # If no hotel names found, skip to the next iteration of the loop

        hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
        hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
        if not hotel_prices:
            continue
        hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
        if not hotel_properties:
            continue
        
    except:
        # Break the loop if no new elements are loaded after scrolling
        break

# Write data to CSV
with open('jessore_hotel.csv', 'w') as f:
    for hotel_name, hotel_currency, display_price, pill_container in zip(hotel_names, hotel_currencies, hotel_prices, hotel_properties):
        line = f"{hotel_name.text},{hotel_currency.text},{display_price.text},{pill_container.text.strip().replace('\n', ' | ')}\n"
        f.write(line)

# Pagination - locate and click on the next page button if available
# Pagination - locate and click on the next page button if available
while is_next_button_present():
    next_button = driver.find_element(By.ID, "paginationNext")
    driver.execute_script("arguments[0].click();", next_button)  # Click using JavaScript
    time.sleep(5)  # Let the new page load
    
    # Refresh elements
    hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
    if not hotel_names:
        continue  # If no hotel names found, skip to the next iteration of the loop

    hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
    hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
    if not hotel_prices:
        continue
    hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
    if not hotel_properties:
        continue
    while True:
        # Scroll down to last elements in lists
        if hotel_names:
            driver.execute_script('arguments[0].scrollIntoView();', hotel_names[-1])
        if hotel_currencies:
            driver.execute_script('arguments[0].scrollIntoView();', hotel_currencies[-1])
        if hotel_prices:
            driver.execute_script('arguments[0].scrollIntoView();', hotel_prices[-1])
        if hotel_properties:
            driver.execute_script('arguments[0].scrollIntoView();', hotel_properties[-1])
        try:
            # Wait for more elements to be loaded
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")) > len(hotel_names))
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")) > len(hotel_currencies))
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")) > len(hotel_prices))
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR,  "div[data-selenium='pill-container']")) > len(hotel_properties))
            # Update lists
            hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
            hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
            hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
            hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
        except:
            # Break the loop if no new elements are loaded after scrolling
            break

driver.quit()
