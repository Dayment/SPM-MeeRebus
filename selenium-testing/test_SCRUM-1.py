import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

def test_apply_wfh_arrangement():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Go to the main page
        driver.get("http://localhost:5173/")

        # Wait for the employee ID input field and enter employee ID (similar to tscrum 4)
        emp_id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "empId"))
        )
        emp_id_input.send_keys("150065")  

        # Find and click the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
        login_button.click()

        # Wait for the page to load after login (confirm by checking presence of an element)
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

        # Select WFH Time (e.g., Full Day)
        wfh_time_dropdown = driver.find_element(By.ID, "wfh-time")
        wfh_time_dropdown.send_keys("Full Day")

        # Select WFH Date (e.g., 2 days from today to ensure it's valid)
        today = datetime.today()
        future_date = today + timedelta(days=2)  
        wfh_date_str = future_date.strftime('%d-%m-%Y')  

        # Select WFH Date in the form
        wfh_date_input = driver.find_element(By.ID, "days")
        wfh_date_input.send_keys(wfh_date_str)  

        # Enter a reason for WFH
        reason_input = driver.find_element(By.ID, "reason")
        reason_input.send_keys("Attending an online training session.")

        # Select Request Type (e.g., Adhoc)
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