import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import requests
import time

# Initialize a counter variable for the number of fill-outs completed
fill_out_count = 1

# Function to simulate a fill-out
def simulate_fill_out():
    # Increment the fill-out count
    global fill_out_count
    fill_out_count += 1

    # Print a message with the fill-out count
    print("************Fill Out Completed*************")
    print(
        f"{fill_out_count} Applicant{'s' if fill_out_count > 1 else ''} details submitted"
    )

# Function to fill a form field and print console messages
def fill_form_field(field_name, value):
    if value:
        print(f"Filled {field_name} with value: {value}")
    else:
        print(f"{field_name} not available")

# Ask the user for the sleep duration in seconds
sleep_duration = int(input("Enter the sleep duration after the final save button (in seconds): "))
# Function to select an option from a dropdown and print console messages
def select_option(driver, dropdown_id, option_text):
    # Wait for the dropdown to be present
    dropdown_locator = (
        By.CSS_SELECTOR, f'#ui-widget_{dropdown_id} .select2-selection--multiple')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(dropdown_locator))

    # Click on the dropdown to open the options
    dropdown = driver.find_element(*dropdown_locator)
    driver.execute_script("arguments[0].scrollIntoView();", dropdown)
    dropdown.click()

    # Scroll multiple times to make sure the option is visible
    for _ in range(3):
        driver.execute_script(
            f"$('#select2-{dropdown_id}-results').scrollTop(10000);")
        # Introduce a small delay to allow content to load (adjust as needed)
        time.sleep(1)

    # Locate the 'Others' option
    others_option_locator = (
        By.XPATH, f"//ul[@id='select2-{dropdown_id}-results']/li[contains(text(), 'Others')]")
    others_option_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(others_option_locator))

    # If 'Others' is not selected, click on it to select
    if 'select2-selected' not in others_option_element.get_attribute('class'):
        # Scroll to the 'Others' option before clicking
        actions = ActionChains(driver)
        actions.move_to_element(others_option_element).perform()

        # Click on the 'Others' option to select
        others_option_element.click()

    # Click outside the dropdown to close it (optional, adjust as needed)
    body = driver.find_element(By.XPATH, '//body')
    body.click()
    print(f"Selected 'Others' option for dropdown with ID: {dropdown_id}")
# Path to your CSV file
csv_file_path = '/Users/adrian/Downloads/TranscomTable_V1.csv'

# Open the website link
website_url = "https://transcom.avature.net/careers/Register?jobId=249&applicationStep=0&source=Vendor&tags=METACOM"

# Create ChromeOptions object
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.binary_location = "/Applications/Google Chrome.app"

# Initialize the WebDriver outside the loop
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(30)


# Create a CSV reader object
with open(csv_file_path, 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Skip the header row if present
    header = next(csv_reader, None)
    header.append('Processed')  # Add 'Processed' column header
    processed_data = []

    # Initialize a flag to track if all rows have been processed
    all_rows_processed = False

    while not all_rows_processed:   
        # Open the website link inside the loop
        driver.get(website_url)
        csv_file.seek(0)
        next(csv_reader, None)  # Skip the header row if present
        # Ask the user for the sleep duration in seconds

        all_rows_processed = True
        for row in csv_reader:
            if '1' in row:
                continue  # Skip rows that have already been processed
            all_rows_processed = False
            print(f"\nProcessing data for {row[2]} {row[1]}")

            # Extract data from each column in the row
            transcom_dropdown_value = row[0]
            last_name = row[1]
            first_name = row[2]
            middle_name = row[3]
            suffix_name = row[4]
            phonenum_name = row[5]
            alternatephonenum_name = row[6]
            email_name = row[7]
            alternateemail_name = row[8]

            # Simulate filling form fields
            fill_form_field("1401", transcom_dropdown_value)
            fill_form_field("1402", last_name)  # Last Name
            fill_form_field("1403", first_name)  # First Name
            fill_form_field("1404", middle_name)  # Middle Name
            fill_form_field("1405", suffix_name)  # Suffix
            fill_form_field("1479", phonenum_name)  # Contact Number
            # Alternate Contact Number
            fill_form_field("1480", alternatephonenum_name)
            fill_form_field("1408", email_name)  # Email
            fill_form_field("1409", alternateemail_name)  # Alternate Email

            # Wait for the Region dropdown to be clickable
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "span.select2-selection__arrow")
                )
            )

            # Check for an overlay element like cookies and close it
            try:
                cookies_overlay = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "cookies"))
                )
                cookies_overlay.click()
                # Introduce a small delay to allow content to load (adjust as needed)
                time.sleep(2)  # Adjust the time as needed
            except:
                pass  # Continue if no overlay is found or if it fails to close

            # Scroll the dropdown into view
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", dropdown)

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(dropdown).click().perform()

            # Display data from the applicants table
            desired_option_text = row[9]

            # Wait for the desired option to be clickable
            desired_option = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f"//li[contains(text(), '{desired_option_text}')]")
                )
            )

            desired_option.click()
            print(f"Selected {desired_option_text} in the dropdown")

            # Identifier for Province dropdown
            province_dropdown_identifier = "1412"

            # Dynamic CSS selector for the Province dropdown
            province_dropdown_css_selector = f"span.select2Container{
                province_dropdown_identifier} .select2-selection__arrow"

            # Wait for the Province dropdown to be clickable
            province_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, province_dropdown_css_selector)
                )
            )

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(
                province_dropdown).click().perform()

            # Display data from the applicants table
            desired_province_option_text = row[10]

            # Wait for the desired option in Province to be clickable
            desired_province_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//li[contains(text(), '{desired_province_option_text}')]",
                    )
                )
            )

            # Click on the desired Province option
            desired_province_option.click()
            print(f"Selected {desired_province_option_text} in the Province dropdown")

            # Identifier for City/Municipality dropdown
            city_dropdown_identifier = "1413"

            # Dynamic CSS selector for the City/Municipality dropdown
            city_dropdown_css_selector = f"span.select2Container{
                city_dropdown_identifier} .select2-selection__arrow"

            # Wait for the City/Municipality dropdown to be clickable
            city_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, city_dropdown_css_selector)
                )
            )

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(
                city_dropdown).click().perform()

            # Display data from the applicants table
            desired_city_option_text = row[11]

            # Wait for the desired option in City/Municipality to be clickable
            desired_city_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     f"//li[contains(text(), '{desired_city_option_text}')]")
                )
            )

            # Click on the desired City/Municipality option
            desired_city_option.click()
            print(f"Selected {desired_city_option_text} in the City/Municipality dropdown")

            # Fill House Number and Street Address fields
            fill_form_field("1414", row[12])
            print(f"Filled House Number and Street Address with value: {row[12]}")

            # Fill Zip Code fields
            fill_form_field("1415", row[13])
            print(f"Filled Zip Code with value: {row[13]}")

            # Find and select a value in the What is your highest educational attainment? dropdown
            educational_dropdown = driver.find_element(By.NAME, "1416")
            educational_select = Select(educational_dropdown)
            fill_form_field("1416", row[14])
            print(f"Selected {row[14]} in the Educational Attainment dropdown")

            # Identifier for How did you learn about Transcom open positions? dropdown
            learn_about_transcom_dropdown_identifier = "1417"

            # Dynamic CSS selector for How did you learn about Transcom dropdown
            learn_about_transcom_dropdown_css_selector = f"span.select2Container{
                learn_about_transcom_dropdown_identifier} .select2-selection__arrow"

            # Wait for How did you learn about Transcom dropdown to be clickable
            learn_about_transcom_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, learn_about_transcom_dropdown_css_selector)
                )
            )

            # Use ActionChains to move to the element and click
            ActionChains(driver).move_to_element(
                learn_about_transcom_dropdown
            ).click().perform()

            # Display the data from applicants table
            desired_learn_about_option_text = row[15]

            # Wait for the desired option in How did you learn about Transcom to be clickable
            desired_learn_about_option = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//li[contains(text(), '{desired_learn_about_option_text}')]",
                    )
                )
            )

            # Click on the desired option in How did you learn about Transcom
            desired_learn_about_option.click()
            print(f"Selected {desired_learn_about_option_text} in the Learn about Transcom dropdown")

            # Fill the Were you referred by someone to apply in Transcom? fields
            is_referred_dropdown = driver.find_element(By.NAME, "1418")
            is_referred_select = Select(is_referred_dropdown)
            fill_form_field("1418", row[16])
            print(f"Selected {row[16]} in the Referred dropdown")

            # Find and select a value in the Referred by dropdown
            referred_by_dropdown = driver.find_element(By.NAME, "1419")
            referred_by_select = Select(referred_by_dropdown)
            fill_form_field("1419", "9037")
            print(f"Selected '9037' in the Referred by dropdown")

            # Fill the Please input Full Name of the referrer fields
            fill_form_field("1420", "Metacom")
            print("Filled 'Metacom' in the Referrer Full Name field")

            # Fill the Password fields
            fill_form_field("1421", "Metacom12345")
            print("Filled 'Metacom12345' in the Password field")

            # Fill the Password Confirmation fields
            fill_form_field("1422", "Metacom12345")
            print("Filled 'Metacom12345' in the Password Confirmation field")

            checkbox = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "1423"))
            )

            # Check if there is any overlay element like cookies and close it
            cookies_overlay = driver.find_element(By.CLASS_NAME, "cookies")
            if cookies_overlay.is_displayed():
                cookies_overlay.click()

            # Introduce a small delay to wait for the overlay to disappear
            time.sleep(2)  # Adjust the time as needed

            # Scroll the checkbox into view
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", checkbox)
            checkbox.click()
            print("Checked the checkbox")

            # Assuming driver is your webdriver instance
            save_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "saveButton"))
            )

            # Check if there is any overlay element like cookies and close it
            cookies_overlay = driver.find_element(By.CLASS_NAME, "cookies")
            if cookies_overlay.is_displayed():
                cookies_overlay.click()
            # Introduce a small delay to wait for the overlay to disappear
            time.sleep(2)  # Adjust the time as needed

            # Scroll the save button into view
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", save_button)
            save_button.click()
            print("Clicked the Save button")

            # Fill the Are you 18, Are you 18 eligible to work in the ph?, and Are you amenable to train and/or work onsite? fields
            fill_form_field("1381", "37")
            fill_form_field("1382", "37")
            fill_form_field("1383", "37")

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            have_bpo_exp_dropdown = driver.find_element(By.NAME, "1384")
            have_bpo_exp_select = Select(have_bpo_exp_dropdown)
            fill_form_field("1384", row[20])

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            total_bpo_exp_dropdown = driver.find_element(By.NAME, "1385")
            total_bpo_exp_select = Select(have_bpo_exp_dropdown)
            fill_form_field("1385", row[21])

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            have_work_exp_dropdown = driver.find_element(By.NAME, "1386")
            have_work_exp_select = Select(have_work_exp_dropdown)
            fill_form_field("1386", row[22])

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            total_work_exp_dropdown = driver.find_element(By.NAME, "1387")
            total_work_exp_select = Select(total_work_exp_dropdown)
            fill_form_field("1387", row[23])

            # Find and select a value in the Do you have BPO/Call Center experience? dropdown
            type_of_bpo_dropdown = driver.find_element(By.NAME, "1388")
            total_of_bpo_select = Select(type_of_bpo_dropdown)
            fill_form_field("1388", row[24])

            # Select the "Others" option in both dropdowns using the modified function
            select_option(driver, '1389', 'Others')
            select_option(driver, '1390', 'Others')

            # Set fields with IDs "1391," "1392," and "1393" to be filled with "N/A"
            fill_form_field("1391", "N/A")
            fill_form_field("1392", "N/A")
            fill_form_field("1393", "N/A")
            fill_form_field("1394", "38")
            fill_form_field("1397", "37")

            # Get the current date
            current_date = datetime.now()

            # Calculate the date 1 day after the current date
            new_date = current_date + timedelta(days=1)

            # Format the new date as a string in the 'yyyy-mm-dd' format
            formatted_date = new_date.strftime("%Y-%m-%d")

            # Find the input element by its ID
            input_element = driver.find_element(By.ID, "1398")

            # Perform actions on the input element (e.g., entering text)
            input_element.send_keys(formatted_date)
            print(f"Filled Date with value: {formatted_date}")

            # Assuming driver is your webdriver instance
            final_save_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "saveButton"))
            )

            # Check if there is any overlay element like cookies and close it
            cookies_overlay = driver.find_element(By.CLASS_NAME, "cookies")
            if cookies_overlay.is_displayed():
                cookies_overlay.click()
            # Introduce a small delay to wait for the overlay to disappear
            time.sleep(2)  # Adjust the time as needed

            # Scroll the final save button into view
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", final_save_button
            )
            final_save_button.click()
            print("Clicked the Final Save button")


            row[25] = '1'  # Assuming 'Processed' column is at index 25
            processed_data.append(row)

            # Sleep for the specified duration
            time.sleep(sleep_duration)
            
        # If all rows have been processed, break out of the while loop
        if all_rows_processed:
            break
        simulate_fill_out()

        # Write the processed_data back to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file_write:
            csv_writer = csv.writer(csv_file_write)
            csv_writer.writerow(header)
            csv_writer.writerows(processed_data)
            print("Loop iteration completed. Restarting the loop...")