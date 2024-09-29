import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

'''
This script uses a chrome webdriver that requires Chrome browser version 115 and newer is being used
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
    driver.get('http://localhost:5173/')
    
    # Find the input element by id and type in the employee ID
    emp_id_input = driver.find_element(By.ID, "empId")
    emp_id_input.send_keys("150065")

    # Find the Login button by class name and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # Add a wait to ensure the page is loaded after login
    time.sleep(5)  # Adjust this as needed for your page load time

    # Check if login was successful by looking for one of the buttons on the next page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary")))
        print("Login successful.")
    except (NoSuchElementException, TimeoutException):
        print("Login failed.")
        driver.quit()
        exit()

    # Wait for 10 seconds
    time.sleep(2)

    # Explicit wait for the Previous button
    try:
        prev_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Previous')]"))
        )
        next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        month_dropdown = driver.find_element(By.ID, "dropdownMonth")
    except TimeoutException:
        print("Previous or Next button not found.")
        driver.quit()
        exit()

    # Check the current month (should be September)
    current_month = month_dropdown.text
    if current_month != "September":
        print("Initial month is not September.")
        driver.quit()
        exit()

    # Click "Previous" and check if the month changes to August
    prev_button.click()
    time.sleep(2)  # Wait for UI update
    updated_month = month_dropdown.text
    if updated_month == "August":
        print("Previous month navigation successful.")
        # Reset back to September by clicking "Next"
        next_button.click()
        time.sleep(2)
    else:
        print("Previous month navigation failed.")
        driver.quit()
        exit()

    # Click "Next" and check if the month changes to October
    next_button.click()
    time.sleep(2)  # Wait for UI update
    updated_month = month_dropdown.text
    if updated_month == "October":
        print("Next month navigation successful.")
        # Reset back to September by clicking "Previous"
        prev_button.click()
        time.sleep(2)
    else:
        print("Next month navigation failed.")
        driver.quit()
        exit()

    # If both checks pass
    print("Previous and Next month navigation successful.")

finally:
    # Quit the driver (optional)
    driver.quit()
