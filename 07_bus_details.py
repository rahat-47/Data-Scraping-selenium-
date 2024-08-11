import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.shohoz.com/booking/bus/search?fromcity=Dhaka&tocity=Sylhet&doj=14-May-2024&dor=21-May-2024")
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
trip_details = wait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class="op_name shohoz_green"]')))
dep_time = wait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[class="tbl_col3 border-fix-seat"]')))
arr_time= wait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[class="tbl_col4 border-fix-seat"]')))
aval_seat= wait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[class="tbl_col5 border-fix-seat shohoz_green"]')))
ticket_price = wait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class="fare_li"]')))

while True:
    # Scroll down to the last elements in the lists
    driver.execute_script('arguments[0].scrollIntoView();', trip_details[-1])
    driver.execute_script('arguments[0].scrollIntoView();', dep_time[-1])
    driver.execute_script('arguments[0].scrollIntoView();', arr_time[-1])
    driver.execute_script('arguments[0].scrollIntoView();', aval_seat[-1])
    driver.execute_script('arguments[0].scrollIntoView();', ticket_price[-1])
    
    try:
        # Wait for more elements to be loaded
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'li[class="op_name shohoz_green"]')))) > len(trip_details))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td[class="tbl_col3 border-fix-seat"]')))) > len(dep_time))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td[class="tbl_col4 border-fix-seat"]')))) > len(arr_time))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td[class="tbl_col5 border-fix-seat shohoz_green"]')))) > len(aval_seat))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'li[class="fare_li"]')))) > len(ticket_price))
        

        # Update lists
        if driver.find_elements(By.CSS_SELECTOR, 'li[class="op_name shohoz_green"]') == None:
            continue
        trip_details = driver.find_elements(
            By.CSS_SELECTOR, 'li[class="op_name shohoz_green"]')
        dep_time = driver.find_elements(
            By.CSS_SELECTOR, 'td[class="tbl_col3 border-fix-seat"]')
        arr_time = driver.find_elements(
            By.CSS_SELECTOR, 'td[class="tbl_col4 border-fix-seat"]')
        aval_seat = driver.find_elements(
            By.CSS_SELECTOR, 'td[class="tbl_col5 border-fix-seat shohoz_green"]')  
        ticket_price = driver.find_elements(
            By.CSS_SELECTOR, 'li[class="fare_li"]')

    except:
        # Break the loop if no new elements are loaded after scrolling
        break

# Write data to CSV with UTF-8 encoding
with open('13_dhaka_to_sylhet.csv', 'w', encoding='utf-8') as f:
    for bus_name, dept_time, arrv_time, fixed_seat, price in zip(trip_details, dep_time, arr_time, aval_seat, ticket_price):
        line = f"{bus_name.text},{dept_time.text},{arrv_time.text},{fixed_seat.text},{price.text.strip().replace('\n', ' | ')}"
        f.write(line + '\n')  # Add newline character to separate rows

print(len(trip_details))
