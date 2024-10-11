from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

# Setup the WebDriver (ensure you have the right driver for your browser)
browser = webdriver.Chrome()

try:
    # Maximize the browser window
    browser.maximize_window()

    # 1) Go to http://localhost:5173/
    browser.get("http://localhost:5173/")
    
    # 2) Find the employee ID input field and enter the ID "150065"
    emp_id_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "empId"))
    )
    emp_id_input.send_keys("150065")
    
    # Find the login button and click it
    login_button = browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # 3) Wait until the calendar is loaded after login to confirm successful login
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
    )
    print("Login successful.")
    
    # 4) Wait for the "Application History" link to be clickable, and then click it
    application_history_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link[href='/history']"))
    )
    application_history_link.click()
    
    # 5) Pause for 5 seconds to ensure the history page has loaded
    time.sleep(5)

    # 6) Find the row with <td>11/1/2024, 9:00:00 AM</td> and get the Cancel button
    arrangement_row = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='11/1/2024, 9:00:00 AM']/.."))
    )

    cancel_button = arrangement_row.find_element(By.XPATH, ".//button[contains(@class, 'btn-danger')]")
    cancel_button.click()
    
    print("Clicked Cancel Arrangement button.")

    # 7) Verify that the Cancel button is no longer present
    time.sleep(2)  # Wait for changes to take effect
    try:
        WebDriverWait(browser, 5).until(
            EC.invisibility_of_element((By.XPATH, ".//button[contains(@class, 'btn-danger')]"))
        )
        print("Cancel button no longer visible, as expected.")
    except:
        print("Error: Cancel button is still present.")

    # 8) Reset the arrangement with arrangement_id=10 via API call
    reset_url = "http://localhost:5000/arrangement/test_scrum_8_reset_arrangement_status/10"
    response = requests.put(reset_url)

    if response.status_code == 200:
        print("Arrangement reset successfully.")
    else:
        print(f"Failed to reset arrangement: {response.status_code}")

    # 9) Pause for observation
    time.sleep(5)

finally:
    # Close the browser after test
    browser.quit()
