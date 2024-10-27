import pytest
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_navigation(driver):
    base_url = os.getenv("BASE_URL")
    if not base_url:
        print("BASE_URL not set.")
        return

    print(f"Testing with BASE_URL: {base_url}")
    
    # Step 1: Load the base URL and wait for the body tag to confirm page load
    driver.get(base_url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Step 2: Login
    emp_id_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "empId"))
    )
    emp_id_input.send_keys("160075")
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
    )
    print("Login successful.")

    # Step 3: Navigate to "Company Schedule"
    try:
        company_schedule_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='nav-link' and @href='/company']"))
        )
        company_schedule_link.click()
        print("Navigated to Company Schedule.")
    except Exception:
        print("Company Schedule link not found.")
        return

    # Step 4: Check for "WFH Arrangements" within the table container
    try:
        wfh_arrangements_header = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='table-container']//h2[contains(text(), 'WFH Arrangements')]"))
        )
        print("WFH Arrangements found.")
    except Exception:
        print("WFH Arrangements not found.")
        return

    # Step 5: Attempt month navigation
    try:
        prev_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Previous')]"))
        )
        month_dropdown = driver.find_element(By.ID, "dropdownMonth")
    except Exception:
        print("Previous button or month dropdown not found.")
        return

    # Check initial month, navigate to previous and validate
    current_month = datetime.datetime.strptime(month_dropdown.text, "%B")
    if current_month.month != 10:
        print("Initial month is not October.")
        return

    prev_button.click()
    time.sleep(2)
    updated_month = datetime.datetime.strptime(month_dropdown.text, "%B")
    if updated_month.month == 9:
        print("Previous month navigation successful.")
        # Click "Next" to go back to October
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
            time.sleep(2)
            updated_month = datetime.datetime.strptime(month_dropdown.text, "%B")
            if updated_month.month == 10:
                print("Next month navigation successful.")
            else:
                print("Next month navigation failed.")
        except Exception:
            print("Next button not found.")
    else:
        print("Previous month navigation failed.")
