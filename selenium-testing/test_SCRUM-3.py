from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta

# Set up Chrome WebDriver
driver = webdriver.Chrome()

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

def refresh_page():
    driver.refresh()
    time.sleep(2)
    print("Page refreshed successfully.")

def verify_table_results(team, sub_team=None):
    # Wait for the table to load
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
    )
    
    # Get all rows in the table
    rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
    
    if len(rows) == 0:
        print(f"No results found for team: {team}, sub-team: {sub_team}")
        return
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 4:  # Ensure we have enough cells
            continue
        
        department = cells[2].text.strip().lower()
        position = cells[3].text.strip().lower()
        
        if team != "All":
            assert team.lower() in department, f"Department '{department}' does not match team '{team}'"
        
        if sub_team:
            assert sub_team.lower() in position, f"Position '{position}' does not match sub-team '{sub_team}'"
    
    print(f"Table results verified for team: {team}, sub-team: {sub_team}")


def test_navigation():
    driver.maximize_window()
    # Visit the local page
    driver.get("http://localhost:5173")  # Update this URL to your actual local setup

    # Wait for the employee ID input field and enter employee ID
    emp_id_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "empId"))
    )
    emp_id_input.send_keys("160075")

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # Wait for the page to load after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
    )
    print("Login successful.")

    # Navigate to the Company Schedule page using XPath
    company_schedule_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/nav/div/div/ul/li[3]/a"))
    )
    company_schedule_link.click()

    time.sleep(1)
    print("Company Schedule page loaded.")


    # Test team and sub-team selection
    for team, sub_teams in team_structure.items():
        # Select main team
        team_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropdownTeam"))
        )
        team_dropdown.click()
        
        team_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{team}')]"))
        )
        team_option.click()
        
        print(f"Selected team: {team}")

        # Verify table results for main team
        verify_table_results(team)

        if sub_teams:
            # Determine the correct sub-team dropdown ID
            if team == "System Solutioning":
                subteam_dropdown_id = "dropdownsyssTeam"
            elif team == "Engineering":
                subteam_dropdown_id = "dropdownengTeam"
            elif team == "HR":
                subteam_dropdown_id = "dropdownhrTeam"
            else:
                continue  # Skip if no sub-teams

            for sub_team in sub_teams:
                subteam_dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, subteam_dropdown_id))
                )
                subteam_dropdown.click()

                sub_team_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{sub_team}')]"))
                )
                sub_team_option.click()
                
                print(f"  Selected sub-team: {sub_team}")

                # Verify table results for sub-team
                verify_table_results(team, sub_team)

                # Here you can add additional checks or actions for each sub-team if needed
                time.sleep(1)
    
    

    print("Team and sub-team selection tests completed successfully.")

    refresh_page()

    # Test search functionality
    search_input = driver.find_element(By.CSS_SELECTOR, "input.filter-input-search")
    search_input.send_keys("engineering")
    time.sleep(2)  # Wait for the table to update

    #Verify filtered results
    verify_table_results("engineering")

    print("Search functionality working correctly.")


    # # Test date filtering
    # start_date_input = driver.find_element(By.ID, "start-date")
    # end_date_input = driver.find_element(By.ID, "end-date")

    # today = datetime.now()
    # one_week_later = today + timedelta(days=7)

    # start_date_input.send_keys(today.strftime("%Y-%m-%d"))
    # end_date_input.send_keys(one_week_later.strftime("%Y-%m-%d"))

    # print("Date range set successfully.")


    # Test calendar view (assuming it's implemented)
    calendar = driver.find_element(By.CSS_SELECTOR, ".calendar-container")  # Adjust selector as needed
    assert calendar.is_displayed(), "Calendar view not displayed"

    print("Calendar view visible.")

    print("All tests passed successfully!")
    
    driver.quit()
    # print(f"Test failed: {str(e)}")
    # Optionally, take a screenshot or dump the page source for debugging
    # driver.save_screenshot("error_screenshot.png")
    # with open("error_page_source.html", "w", encoding="utf-8") as f:
    #    f.write(driver.page_source)

