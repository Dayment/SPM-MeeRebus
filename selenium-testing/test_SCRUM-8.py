import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

load_dotenv()

def test_navigation():
    base_url = os.getenv("BASE_URL")

    # Set up Chrome options for headless mode in CI
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for CI environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
    chrome_options.add_argument("--disable-gpu")  # Optional, may improve CI performance

    # Initialize Chrome WebDriver with options
    browser = webdriver.Chrome(options=chrome_options)
    
    # 1) Go to the URL from the environment variable
    browser.get(base_url)

    # Find the input element by id and type in the employee ID
    emp_id_input = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.ID, "empId"))
    )
    emp_id_input.send_keys("150065")

    # Find the Login button by class name and click it
    login_button = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # Add a wait to ensure the page is loaded after login
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
    )
    print("Login successful.")

    # Wait for a bit
    time.sleep(2)

    # Try to navigate to the previous month
    try:
        prev_button = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Previous')]"))
        )
        month_dropdown = browser.find_element(By.ID, "dropdownMonth")
    except TimeoutException:
        print("Previous button not found.")
        return

    # Check if the current month is October
    current_month = month_dropdown.text
    if current_month != "October":
        print("Initial month is not October.")
        return

    # Click the "Previous" button and check if the month changes to September
    prev_button.click()
    time.sleep(2)  # Wait for UI update
    updated_month = month_dropdown.text
    if updated_month == "September":
        print("Previous month navigation successful.")

        # Check for the "Next" button after successfully navigating to the previous month
        try:
            next_button = WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            # Click "Next" and check if the month changes back to October
            next_button.click()
            time.sleep(2)  # Wait for UI update
            updated_month = month_dropdown.text
            if updated_month == "October":
                print("Next month navigation successful.")
            else:
                print("Next month navigation failed.")
        except TimeoutException:
            print("Next button not found.")
    else:
        print("Previous month navigation failed.")

    # Close the browser after test
    browser.quit()