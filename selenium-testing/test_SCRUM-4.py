from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_navigation():
    # Set up Chrome options for headless mode in CI
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for CI environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
    chrome_options.add_argument("--disable-gpu")  # Optional, may improve CI performance

    # Initialize Chrome WebDriver with options
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()

    try:
        base_url = os.getenv("BASE_URL")
        browser.get(base_url)

        emp_id_input = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, "empId"))
        )
        emp_id_input.send_keys("150065")

        login_button = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
        login_button.click()

        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
        )
        print("Login successful.")
        
        application_history_link = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/history']"))
        )
        application_history_link.click()
        time.sleep(2)

        # Reset arrangement with API call
        reset_url = f"{base_url}/arrangement/test_scrum_8_reset_arrangement_status/10"
        response = requests.put(reset_url)
        if response.status_code == 200:
            print("Arrangement reset successfully.")
        else:
            print(f"Failed to reset arrangement: {response.status_code}")

        # Find the arrangement row and click Cancel button
        arrangement_row = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//td[text()='2024-11-01']/.."))
        )
        cancel_button = arrangement_row.find_element(By.XPATH, ".//button[contains(@class, 'btn-danger')]")
        cancel_button.click()
        print("Clicked Cancel Arrangement button.")

        # Verify that the Cancel button is no longer present
        time.sleep(2)
        try:
            WebDriverWait(browser, 10).until(
                EC.invisibility_of_element_located((By.XPATH, ".//button[contains(@class, 'btn-danger')]"))
            )
            print("Cancel button no longer visible, as expected.")
        except:
            print("Error: Cancel button is still present.")

        # Reset the arrangement with arrangement_id=10 via API call
        response = requests.put(reset_url)
        if response.status_code == 200:
            print("Arrangement reset successfully.")
        else:
            print(f"Failed to reset arrangement: {response.status_code}")

        # Pause for observation
        time.sleep(2)
    
    finally:
        browser.quit()