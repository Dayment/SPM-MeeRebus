from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Set up Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Visit the local page
    driver.get("http://localhost:5173")

    # Wait for the employee ID input field and enter employee ID (similar to tscrum 4)
    emp_id_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "empId"))
    )
    emp_id_input.send_keys("160075")  

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block")
    login_button.click()

    # Wait for the page to load after login (confirm by checking presence of an element)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "calendar-container"))
    )
    print("Login successful.")

    # Wait for the header to appear
    # header = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, ".schedule-header"))
    # )

    # Verify if the header contains "Schedule"
    # assert "Company Schedule" in header.text

# Navigate to the Company Schedule page
    company_schedule_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link[href='/company']"))
    )
    company_schedule_link.click()

    time.sleep(1)  
    print("Company Schedule page loaded.")


#     # Interact with department selection
#     department_select = driver.find_element(By.CSS_SELECTOR, "select.department")
#     department_select.send_keys("HR")

#     # Wait for the event list to update
#     event_list = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".event-list"))
#     )

#     # Verify if the event list contains "HR Event"
#     assert "HR Event" in event_list.text

#     print("Test passed!")

# except Exception as e:
#     print("Test failed:", str(e))

    # Step 2: Wait for the main team dropdown to be visible
    wait = WebDriverWait(driver, 10)
    main_team_dropdown = wait.until(EC.visibility_of_element_located((By.ID, "team-dropdown")))  # Ensure correct ID
    main_team_select = Select(main_team_dropdown)

    # Define expected sub-team options for each main team
    expected_sub_teams = {
        "System Solutioning": {
            "dropdown_id": "syss-team-dropdown",
            "expected_options": ['Developers', 'Support Team']
        },
        "Engineering": {
            "dropdown_id": "eng-team-dropdown",
            "expected_options": ['Senior Engineers', 'Junior Engineers', 'Call Centre', 'Operation Planning Team']
        },
        "HR": {
            "dropdown_id": "hr-team-dropdown",
            "expected_options": ['HR Team', 'L&D team', 'Admin Team']
        },
        "Sales": {
            "dropdown_id": None,  # No sub-team expected for Sales
            "expected_options": None
        },
        "Consultancy": {
            "dropdown_id": None,  # No sub-team expected for Consultancy
            "expected_options": None
        },
        # Add more main teams and their corresponding sub-teams if applicable
    }

    # Step 3: Iterate through each main team option and check sub-team dropdowns
    for main_team_option in main_team_select.options:
        main_team = main_team_option.text
        
        # Select the main team
        main_team_select.select_by_visible_text(main_team)
        
        if main_team in expected_sub_teams:
            sub_team_info = expected_sub_teams[main_team]
            
            # Check if there is an associated sub-team dropdown
            if sub_team_info["dropdown_id"]:
                # Wait for the sub-team dropdown to be visible
                sub_team_dropdown = wait.until(EC.visibility_of_element_located((By.ID, sub_team_info["dropdown_id"])))
                sub_team_select = Select(sub_team_dropdown)

                # Get the actual sub-team options
                actual_sub_team_options = [option.text for option in sub_team_select.options]
                expected_sub_team_options = sub_team_info["expected_options"]

                # Step 4: Assert that the actual options match the expected ones
                assert actual_sub_team_options == expected_sub_team_options, \
                    f"Mismatch for {main_team}: Expected {expected_sub_team_options}, but got {actual_sub_team_options}"
                print(f"Sub-team options for {main_team} are correct: {actual_sub_team_options}")
            else:
                print(f"No sub-team dropdown expected for {main_team}, as expected.")
        else:
            print(f"Main team {main_team} not found in expected_sub_teams mapping.")
finally:
# Close the browser
    driver.quit()