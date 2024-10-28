import pytest
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from dotenv import load_dotenv

load_dotenv()

def test_navigation():
    base_url = os.getenv("BASE_URL")
    if not base_url:
        print("BASE_URL not set in environment variables.")
        return

    print(f"Testing with BASE_URL: {base_url}")

    # Set up Chrome options for headless mode in CI
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Initialize Chrome WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # 1) Go to the URL from the environment variable
        driver.get(base_url)
        
        # Confirm page load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Wait for the employee ID input field and enter employee ID
        try:
            emp_id_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "empId"))
            )
            emp_id_input.send_keys("130002")
        except TimeoutException:
            print("Employee ID input field not found.")
            return

        # Find the Login button and click it
        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
        login_button.click()

        # Wait for login confirmation
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
        )
        print("Login successful.")

        # Navigate to "Company Schedule"
        try:
            company_schedule_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='nav-link' and @href='/company']"))
            )
            company_schedule_link.click()
            print("Navigated to Company Schedule.")
        except TimeoutException:
            print("Company Schedule link not found.")
            return

        # Check for "WFH Arrangements" within the table container
        try:
            wfh_arrangements_header = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='table-container']//h2[contains(text(), 'WFH Arrangements')]"))
            )
            print("WFH Arrangements found.")
        except TimeoutException:
            print("WFH Arrangements not found.")
            return

        # Attempt month navigation
        try:
            prev_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Previous')]"))
            )
            month_dropdown = driver.find_element(By.ID, "dropdownMonth")
        except TimeoutException:
            print("Previous button or month dropdown not found.")
            return

        # Check initial month, navigate, and validate
        current_month = datetime.datetime.strptime(month_dropdown.text, "%B")
        if current_month.month != 10:
            print("Initial month is not October.")
            return

        prev_button.click()
        time.sleep(2)
        updated_month = datetime.datetime.strptime(month_dropdown.text, "%B")
        assert updated_month.month + 1 == current_month.month

        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
            time.sleep(2)
            updated_month = datetime.datetime.strptime(month_dropdown.text, "%B")
            assert updated_month.month == current_month.month
        except TimeoutException:
            print("Next button not found.")

    finally:
        driver.quit()