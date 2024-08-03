# Facility Data Scraper for CatchCorner
This project is a web scraper built using Selenium to extract facility data from the CatchCorner website. The script collects information such as facility names, locations, available sports, images, and other relevant details and stores them in a CSV file for further analysis or use.

## Features
Extract facility information from CatchCorner.
Handles dynamic content and pop-ups.
Navigate through multiple locations and facilities.
Supports extraction of sports options and their corresponding details.
Stores the extracted data in a structured CSV file.

## Requirements
Python 3.6+
Selenium 4.0+
Google Chrome browser
*ChromeDriver is now included*

## Dependencies
Install the required Python packages using pip:

bash
Copy code
`pip install selenium`

## How to Use
1) Configure Script Variables:
Update the csv_file variable to specify the output CSV file name.
Adjust wait_time, include_time_data, number_of_months, and testing_number_of_times as needed.
2) The script runs on a location basis meaning it scrapes per location so pick the location you want to scrape the data from.
3) Run the Script
4) Remove duplicates as you wish or if program crashes, rerun script. You can also rerun the script and change the facility index to change your start point.


## Variable Declarations
driver: Initializes the Chrome WebDriver.
current_year: Captures the current year.
wait_time: Sets the wait time for elements to load.
include_time_data, number_of_months, testing_number_of_times: Control various aspects of data extraction.
csv_file: Specifies the name of the CSV file for storing the data.

## Helper Functions
click_after_wait(find_by): Clicks an element after waiting for it to be present.
click_specified_element_after_wait(find_by, element): Clicks a specified element after waiting for it to be present.
scroll_element(element, scroll_pause_time): Scrolls a specific element down.
add_availability(year, month, day): Adds a new day to the availability dictionary.
update_availability_time_slot(year, month, day, time_slot): Updates the availability dictionary with a new time slot.
add_to_csv(...): Adds data to the CSV file.

## Main Script Logic
Navigate to CatchCorner:
Open the CatchCorner intro page.
Handle any pop-ups that appear.

**Location Handling:**
Click the location dropdown and retrieve the list of locations.
Iterate through each location to gather facility information.

**Facility Handling:**
Refresh the facility list to prevent stale element exceptions.
Click through the facilities and navigate to their detail pages.
Extract information such as facility title, location, sports options, and images.

**Data Extraction:**
For each facility, gather relevant details and append them to the CSV file.

## Notes
The script includes error handling to manage exceptions like TimeoutException, StaleElementReferenceException, and ElementClickInterceptedException.
Ensure that the webpage structure and class names have not changed, as this may affect the script's ability to locate elements.
This script will crash at times since there can be server-side issues with web scraping as well.
The script also is forced to scape duplicates so the facility index may not match up to your original assumption.

## Future Enhancements
Implement more robust error handling and logging.
Add support for other web browsers.
Optimize the script for faster data extraction.
License
This project is licensed under the MIT License.
