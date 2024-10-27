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
    print(f"Testing with BASE_URL: {base_url}")
    
    # Set up Chrome options for headless mode in CI
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for CI environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
    chrome_options.add_argument("--disable-gpu")  # Optional, improves performance in CI

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Go to the URL from the environment variable
        driver.get(base_url)
        
        # Confirm that the page has loaded by checking for the presence of the body tag
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Wait for the employee ID input field and enter employee ID
        emp_id_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "empId"))
        )
        emp_id_input.send_keys("130002")
        
        # Find the Login button by class name and click it
        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
        login_button.click()

        # Add a wait to ensure the page is loaded after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
        )
        print("Login successful.")
        
        # Continue with additional navigation or test steps as required
        # ...

    except TimeoutException as e:
        print("An element was not found within the time limit.", e)
    finally:
        driver.quit()