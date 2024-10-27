import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

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
        driver.get(base_url)  # Use URL from environment variable

        # Wait for employee ID input field and enter employee ID
        emp_id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "empId"))
        )
        emp_id_input.send_keys("150065")

        # Find and click the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
        login_button.click()

        # Wait for page to load after login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
        )
        print("Login successful.")

        # Navigate to the Apply for WFH Arrangement page
        apply_arrangement_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link[href='/apply']"))
        )
        apply_arrangement_link.click()
        time.sleep(1)
        print("Apply Arrangement page loaded.")

        # Fill out WFH application form
        wfh_time_dropdown = driver.find_element(By.ID, "wfh-time")
        wfh_time_dropdown.send_keys("Full Day")

        today = datetime.today()
        future_date = today + timedelta(days=2)
        wfh_date_str = future_date.strftime('%d-%m-%Y')
        wfh_date_input = driver.find_element(By.ID, "days")
        wfh_date_input.send_keys(wfh_date_str)

        reason_input = driver.find_element(By.ID, "reason")
        reason_input.send_keys("Attending an online training session.")

        request_type_dropdown = driver.find_element(By.ID, "request-type")
        request_type_dropdown.send_keys("Adhoc")

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        submit_button.click()

        # Wait for the confirmation alert
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        assert "WFH request submitted" in alert.text
        alert.accept()

        print(f"Test passed: WFH arrangement applied successfully for {wfh_date_str}.")
    
    finally:
        driver.quit()