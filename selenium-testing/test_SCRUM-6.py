import pytest
import time
import requests
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_navigation():
    url = "http://48.218.168.55:5173/"

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(url)
    
    # Find the input element by id and type in the employee ID
    emp_id_input = driver.find_element(By.ID, "empId")
    emp_id_input.send_keys("140008")

    # Find the Login button by class name and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # Add a wait to ensure the page is loaded after login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "calendar-container")))
    logger.info("Login successful.")

    # Navigate to "WFH Approval"
    try:
        # Click the "Applications" dropdown to reveal the "WFH Approval" link
        applications_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Applications')]"))
        )
        applications_dropdown.click()

        # Now locate and click the "WFH Approval" link
        wfh_approval_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='dropdown-item' and @href='/managerapproval']"))
        )
        wfh_approval_link.click()
        logger.info("Navigated to WFH Approval Page.")
    except TimeoutException:
        logger.error("WFH Approval link not found.")
        return

    # Wait for a bit
    time.sleep(2)

    reset_url = "https://earnest-grace-production-04af.up.railway.app/arrangement/test_scrum_8_reset_arrangement_status/63"
    response = requests.put(reset_url)

    if response.status_code == 200:
        logger.info("Arrangement reset successfully.")
    else:
        logger.error(f"Failed to reset arrangement: {response.status_code}")
    time.sleep(2)

    driver.refresh()
    arrangement_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='2024-12-12']/.."))
    )

    approve_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class, 'btn-primary')]"))
    )
    approve_button.click()
    
    logger.info("Clicked Approve Arrangement button.")
    time.sleep(2)

    # Refresh the page
    driver.refresh()

    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.XPATH, ".//button[contains(@class, 'btn-primary')]"))
        )
        logger.info("Approve button no longer visible, as expected.")
    except TimeoutException:
        raise Exception("Error: Approve button is still present.")


    reset_url = "https://earnest-grace-production-04af.up.railway.app/arrangement/test_scrum_8_reset_arrangement_status/63"
    response = requests.put(reset_url)

    if response.status_code == 200:
        logger.info("Arrangement reset successfully.")
    else:
        logger.error(f"Failed to reset arrangement: {response.status_code}")
    
    time.sleep(2)
    driver.refresh()
    withdraw_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//button[contains(@class, 'btn-danger')]"))
    )
    withdraw_button.click()
    time.sleep(2)
    
    logger.info("Clicked Withdraw Arrangement button.")
    
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-footer']//button[contains(@class, 'btn-primary') and text()='Submit']"))
    )
    submit_button.click()
    time.sleep(2)

    # Refresh the page
    driver.refresh()

    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element((By.XPATH, ".//button[contains(@class, 'btn-danger')]"))
        )
        logger.info("Withdraw button no longer visible, as expected.")
    except TimeoutException:
        raise Exception("Error: Withdraw button is still present.")

    time.sleep(2)

    reset_url = "https://earnest-grace-production-04af.up.railway.app/arrangement/test_scrum_8_reset_arrangement_status/63"
    response = requests.put(reset_url)

    if response.status_code == 200:
        logger.info("Arrangement reset successfully.")
    else:
        logger.error(f"Failed to reset arrangement: {response.status_code}")

    driver.quit()