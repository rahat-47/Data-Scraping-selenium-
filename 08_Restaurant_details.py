import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/search/restaurants+near+rangpur/?entry=ttu&hl=en")
# Wait for the page to load
time.sleep(5)

# Function to check if the next button is present
def is_next_button_present():
    try:
        driver.find_element(By.ID, "paginationNext")
        return True
    except NoSuchElementException:
        return False

# Find all restaurant names on the first page
restaurant_name = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'hfpxzc')))
restaurant_rating = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ZkP5Je')))
restaurant_location = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.W4Efsd > span:nth-child(2) > span:nth-child(2)')))

while True:
    # Scroll down to the last elements in the lists
    driver.execute_script('arguments[0].scrollIntoView();', restaurant_name[-1])
    driver.execute_script('arguments[0].scrollIntoView();', restaurant_rating[-1])
    driver.execute_script('arguments[0].scrollIntoView();', restaurant_location[-1])
    try:
        # Wait for more elements to be loaded
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'hfpxzc')))) > len(restaurant_name))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'ZkP5Je')))) > len(restaurant_rating))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.W4Efsd > span:nth-child(2) > span:nth-child(2)')))) > len(restaurant_location))

        # Update lists
        restaurant_name = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        restaurant_rating = driver.find_elements(By.CLASS_NAME, 'ZkP5Je')
        restaurant_location = driver.find_elements(By.CSS_SELECTOR, 'div.W4Efsd > span:nth-child(2) > span:nth-child(2)')

    except:
        # Break the loop if no new elements are loaded after scrolling
        break
with open('restaurant_rangpur.csv', 'w', encoding='utf-8') as f:
 for rest_name, rest_rating, rest_location in zip(restaurant_name, restaurant_rating, restaurant_location):
    line=f"{rest_name.get_attribute("aria-label").strip().replace(',', ' | ')}, {rest_rating.get_attribute("aria-label").strip().replace(',', ' | ')}, {rest_location.text.strip().replace(',', ' | ')}"
    f.write(line + '\n')
print(len(restaurant_name))
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait as wait
# from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Chrome()
# driver.get("https://www.google.com/maps/search/restaurants+near+rangamati/?entry=ttu&hl=en")
# time.sleep(5)

# # Function to check if the next button is present
# def is_next_button_present():
#     try:
#         driver.find_element(By.ID, "paginationNext")
#         return True
#     except NoSuchElementException:
#         return False

# # Find initial restaurant elements
# restaurant_name = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'hfpxzc')))
# restaurant_rating = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ZkP5Je')))
# restaurant_location = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.W4Efsd > span:nth-child(2) > span:nth-child(2)')))

# while True:
#     try:
#         # Scroll to the last elements in the lists
#         driver.execute_script('arguments[0].scrollIntoView();', restaurant_name[-1])
#         driver.execute_script('arguments[0].scrollIntoView();', restaurant_rating[-1])
#         driver.execute_script('arguments[0].scrollIntoView();', restaurant_location[-1])
        
#         # Wait for more elements to be loaded
#         new_restaurant_name = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'hfpxzc')))
#         new_restaurant_rating = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ZkP5Je')))
#         new_restaurant_location = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.W4Efsd > span:nth-child(2) > span:nth-child(2)')))
        
#         # Break the loop if no new elements are loaded after scrolling
        
#         # Update lists
#         restaurant_name = new_restaurant_name
#         restaurant_rating = new_restaurant_rating
#         restaurant_location = new_restaurant_location

#     except:
#         break

# with open('restaurant_rangamati.csv', 'w', encoding='utf-8') as f:
#     for rest_name, rest_rating, rest_location in zip(restaurant_name, restaurant_rating, restaurant_location):
#         name = rest_name.get_attribute("aria-label").strip().replace(',', ' | ')
#         rating = rest_rating.get_attribute("aria-label")
#         # Extract the address from the correct span element
#         address = rest_location.text.strip().replace(',', ' | ')
#         line = f"{name}, {rating}, {address}"
#         f.write(line + '\n')

# print(len(restaurant_name))

# driver.quit()
