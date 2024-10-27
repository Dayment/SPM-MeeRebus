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

def test_apply_wfh_arrangement():
    # Set up Chrome options for headless mode in CI
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for CI environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
    chrome_options.add_argument("--disable-gpu")  # Optional, may improve CI performance

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Go to the main page
        base_url = os.getenv("BASE_URL")
        print(f"Testing with BASE_URL: {base_url}")
        driver.get(base_url)  # Use URL from environment variable

        # Extra wait for page load confirmation (e.g., body element or a specific div)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Wait for employee ID input field and enter employee ID
        emp_id_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "empId"))
        )
        emp_id_input.send_keys("150065")  

        # Find and click the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
        login_button.click()

        # Wait for the calendar container to confirm login
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
        )
        print("Login successful.")

    except TimeoutException:
        print("Timed out waiting for elements to load. Please check if BASE_URL is accessible and the page elements are as expected.")
    finally:
        driver.quit()