import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# argument parser to accept URL from the command line
parser = argparse.ArgumentParser(description='Selenium test for navigating the website.')
parser.addoption('--url', help='URL of the site to test', required=True)
args = parser.parse_args()

'''
This script uses a chrome webdriver that requires Chrome browser version 115 or newer
Ensure that selenium library is installed:
pip install selenium

Run the following command: 
python test_SCRUM-8.py
'''

# Set up the path to the ChromeDriver using the Service class
service = Service('./chromedriver.exe')  # Path to ChromeDriver (assuming it's in the same folder)

# Initialize WebDriver
driver = webdriver.Chrome(service=service)

try:
    # Go to the website
    driver.get(args.url)
    
    # Find the input element by id and type in the employee ID
    emp_id_input = driver.find_element(By.ID, "empId")
    emp_id_input.send_keys("150065")

    # Find the Login button by class name and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # Add a wait to ensure the page is loaded after login
    time.sleep(2)  # Adjust this as needed for your page load time

    # Check if login was successful by waiting for the presence of an element with class "calendar-container"
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "calendar-container")))
        print("Login successful.")
    except (NoSuchElementException, TimeoutException):
        print("Login failed. 'calendar-container' not found.")
        driver.quit()
        exit()

    # Wait for 10 seconds
    time.sleep(2)

    # Explicit wait for the Previous button
    try:
        prev_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Previous')]"))
        )
        month_dropdown = driver.find_element(By.ID, "dropdownMonth")
    except TimeoutException:
        print("Previous button not found.")
        driver.quit()
        exit()

    # Check the current month (should be October)
    current_month = month_dropdown.text
    if current_month != "October":
        print("Initial month is not October.")
        driver.quit()
        exit()

    # Click "Previous" and check if the month changes to September
    prev_button.click()
    time.sleep(2)  # Wait for UI update
    updated_month = month_dropdown.text
    if updated_month == "September":
        print("Previous month navigation successful.")
        
        # Now check for the Next button directly after successfully navigating to the Previous month
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            # Click "Next" and check if the month changes to October
            next_button.click()
            time.sleep(2)  # Wait for UI update
            updated_month = month_dropdown.text
            if updated_month == "October":
                print("Next month navigation successful.")
            else:
                print("Next month navigation failed.")
                driver.quit()
                exit()

        except TimeoutException:
            print("Next month navigation failed.")
            driver.quit()
            exit()

    else:
        print("Previous month navigation failed.")
        driver.quit()
        exit()

finally:
    # Quit the driver (optional)
    time.sleep(2)
    driver.quit()
