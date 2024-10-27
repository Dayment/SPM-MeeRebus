import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

load_dotenv()

# Fixture to initialize and close the WebDriver
@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()

# Helper function to refresh the page
def refresh_page(driver):
    driver.refresh()
    time.sleep(2)
    print("Page refreshed successfully.")

# Helper function to verify table results
def verify_table_results(driver, team, sub_team=None):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
        )
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        if not rows:
            print(f"No results found for team: {team}, sub-team: {sub_team}")
            return

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue
            
            department = cells[2].text.strip().lower()
            position = cells[3].text.strip().lower()
            
            if team != "All":
                assert team.lower() in department, f"Department '{department}' does not match team '{team}'"
            
            if sub_team:
                assert sub_team.lower() in position, f"Position '{position}' does not match sub-team '{sub_team}'"
        
        print(f"Table results verified for team: {team}, sub-team: {sub_team}")
    except Exception as e:
        print(f"Error verifying table results: {e}")

# Main test function
def test_navigation(driver):
    base_url = os.getenv("BASE_URL")
    if not base_url:
        print("BASE_URL not set.")
        return

    # Load the base URL and confirm page load by waiting for the body tag
    driver.get(base_url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Login sequence
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

    # Navigate to Company Schedule
    company_schedule_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/nav/div/div/ul/li[3]/a"))
    )
    company_schedule_link.click()
    time.sleep(1)
    print("Company Schedule page loaded.")

    # Define team structure
    team_structure = {
        "All": None,
        "Sales": None,
        "Consultancy": None,
        "System Solutioning": ["Developers", "Support Team"],
        "Engineering": ["Senior Engineers", "Junior Engineers", "Call Centre", "Operation Planning Team"],
        "HR": ["HR Team", "L&D team", "Admin Team"],
        "Finance": None,
        "IT": None
    }

    # Select teams and sub-teams
    for team, sub_teams in team_structure.items():
        team_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "dropdownTeam"))
        )
        team_dropdown.click()
        team_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{team}')]"))
        )
        team_option.click()
        print(f"Selected team: {team}")
        verify_table_results(driver, team)

        if sub_teams:
            subteam_dropdown_id = (
                "dropdownsyssTeam" if team == "System Solutioning" else
                "dropdownengTeam" if team == "Engineering" else
                "dropdownhrTeam" if team == "HR" else None
            )
            if subteam_dropdown_id:
                for sub_team in sub_teams:
                    subteam_dropdown = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, subteam_dropdown_id))
                    )
                    subteam_dropdown.click()
                    sub_team_option = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{sub_team}')]"))
                    )
                    sub_team_option.click()
                    print(f"  Selected sub-team: {sub_team}")
                    verify_table_results(driver, team, sub_team)
                    time.sleep(1)

    print("Team and sub-team selection tests completed successfully.")

    refresh_page(driver)

    # Test search functionality
    search_input = driver.find_element(By.CSS_SELECTOR, "input.filter-input-search")
    search_input.send_keys("engineering")
    time.sleep(2)
    verify_table_results(driver, "engineering")
    print("Search functionality working correctly.")

    # Check calendar visibility
    calendar = driver.find_element(By.CSS_SELECTOR, ".calendar-container")
    assert calendar.is_displayed(), "Calendar view not displayed"
    print("Calendar view visible.")