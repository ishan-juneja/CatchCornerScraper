from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, \
	NoSuchElementException, TimeoutException
import time, datetime, csv, os, re

# THE QUESTION THEN IS THAT OK WE POPULATE OUR SPREADSHEET
# WE HAVE OUR CSV FILE NOW BUT ONCE WE GET THAT DATA AND RERUN THE SCRIPT
# HOW DO WE MAKE SURE WE ARE PROPERLY NUMBERING OUR DATA
# WE CAN NUMBER BASED OFF THE NAME LIKE MAKE AN ID WITH A CODE IF TAHT MAKES SENSE
# ALSO FURTHERMORE HOW ARE WE UPDATING THE DATA IF WE NEED TO

# ALSO MAKE SURE THAT THE NUMBER OF MONTHS WE WANT IS SPECIFIED


# Variables Declaration
driver = webdriver.Chrome()
driver.get("https://www.catchcorner.com/intro")
current_year = datetime.datetime.now().year  # the year we are on!
wait_time = 5  # this time ensures the element is loaded. Adjust depending on speeds
# This will significantly slow the program down
include_time_data = False
number_of_months = 2
testing_number_of_times = 40
csv_file = 'facility_data_catch_corner_LA_ANA.csv'  # the csv file we are sending to


# Outer Dictionary: Keys are years (e.g., 2023, 2024).
# Second Level Dictionary: Keys are months (e.g., 1, 2, ..., 12).
# Innermost Dictionary: Keys are day numbers (e.g., 1 to 31) and values are lists of available time slots.
# Initialize the availability dictionary

def click_after_wait(find_by):
	try:
		WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, find_by)))
		button = driver.find_element(By.CLASS_NAME, find_by)
		driver.execute_script("arguments[0].click();", button)
	except TimeoutException:
		print("Element not found within the specified wait time using: ", find_by)
		pass



def click_specified_element_after_wait(find_by, element):
	try:
		WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, find_by)))
		driver.execute_script("arguments[0].click();", element)
	except TimeoutException:
		print("Element not found within the specified wait time using: ", find_by)
		pass


def scroll_element(element, scroll_pause_time=1.0):
	"""A method for scrolling a specific element down."""
	last_height = driver.execute_script("return arguments[0].scrollHeight", element)

	while True:
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
		driver.implicitly_wait(scroll_pause_time)

		new_height = driver.execute_script("return arguments[0].scrollHeight", element)
		if new_height == last_height:
			break
		last_height = new_height


# We don't have to worry about getting an incorrect date because it is getting scraped from the website
def add_availability(year, month, day):
	"""
    Adds a new day to the availability dictionary for a given year and month.
    :param year: The year to which the day will be added.
    :param month: The month to which the day will be added.
    :param day: The day to be added.
    """
	if year not in availability:
		availability[year] = {}
	if month not in availability[year]:
		# Assuming 31 days for a new month by default
		availability[year][month] = {day: [] for day in range(1, 32)}
	if day not in availability[year][month]:
		availability[year][month][day] = []


# Update availability time slot with dynamic date addition
def update_availability_time_slot(year, month, day, time_slot):
	add_availability(year, month, day)  # will add availability if
	availability[year][month][day] = time_slot


# Define the function to add data to the CSV file
def add_to_csv(facility_title, city, sport_name, location, street_address, zip_code, google_map_embed, description,
               thumbnail,
               social_image, all_images, hourly_rate, display_price, list_of_sports, link):
	# Define the header
	header = ['Facility Name', 'City', 'Type', 'Location', 'Street Address', 'Zip Code', 'Google Map Embed',
	          'Listing Description', 'Continent', 'Thumbnail', 'Social:Image', 'Listing Images', 'Hourly Rate',
	          'Display Price', 'Sports', 'Booking Link', 'Rentals Page (INTERNAL USE)', 'Rating', 'Approved',
	          'Manager', 'Email (from Host)', 'Picture (from Host)', 'User (from Host)', 'Host Name (from Host)',
	          'Host Email', 'Users', 'Activities', 'Booking Requests', 'SEO:Index', 'SEO:Title',
	          'SEO:Description', 'Social:Title', 'Social:Description', 'SEO:Slug', 'Activity Reviews (from Activities)',
	          'Latitude', 'Longitude']

	# Check if the CSV file exists
	file_exists = os.path.isfile(csv_file)

	# Open the CSV file in append mode
	with open(csv_file, mode='a', newline='') as file:
		writer = csv.DictWriter(file, fieldnames=header)

		# If the file doesn't exist, write the header
		if not file_exists:
			writer.writeheader()
		# Write the data
		writer.writerow({
			'Facility Name': facility_title,
			'City': city,
			'Type': sport_name,
			'Location': location,
			'Street Address': street_address,
			'Zip Code': zip_code,
			'Google Map Embed': google_map_embed,
			'Listing Description': description,
			'Continent': 'North America',
			'Thumbnail': thumbnail,
			'Social:Image': social_image,
			'Listing Images': all_images,
			'Hourly Rate': hourly_rate,
			'Display Price': display_price,
			'Sports': list_of_sports,
			'Booking Link': link,
		})


# Note: CatchCorner has a set amount of locations, and they have facilities so the idea is
# Nested Loops:
# Loop 1: loop through locations
# Loop 2: within each location, we have a list of facilities to loop through
# Loop 3: a location can have multiple sports with different timings, so we must loop through
# Actions: Within loop 3 scope, scrape our information, and we must add our data to a csv
# Loop 4: Get the timings of the location
# We need to loop through all our locations


# If our location isn't shared a pop up may appear
click_after_wait("cc-modal-alert__cancel-icon")

# Switch from the popup if needed
parent = driver.window_handles[0]
driver.switch_to.window(parent)

# Wait for the page to load the locations by clicking the dropdown
click_after_wait("location-bar__text")

# Wait for the locations to popdown
WebDriverWait(driver, wait_time).until(
	EC.presence_of_element_located((By.CLASS_NAME, "location-bar__dropdown-item-title")))
location_list = driver.find_elements(By.CLASS_NAME, "location-bar__dropdown-item-title")

#Manually Change Locations
time.sleep(1)

# Loop 2: Facilities

# Gather facilities for current location
WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, "tile__avl-times")))
facility_list = driver.find_elements(By.CLASS_NAME, "tile__avl-times")

facility_index = -1

number_of_clicks = 9



while True:
	# page_url = driver.current_url
	# print("our current url is: ", page_url)
	#
	# if page_url == "https://www.catchcorner.com/intro":
	# 	pass
	# else:
	# 	driver.get("https://www.catchcorner.com/intro")
	# 	facility_index -= 1
	# 	continue
	driver.get("https://www.catchcorner.com/intro")
	# Wait for the page to load the locations by clicking the dropdown
	click_after_wait("location-bar__text")

	try:  # refresh our locations to prevent stale element exception
		WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CLASS_NAME, "location-bar__dropdown-item-title")))
		location_list = driver.find_elements(By.CLASS_NAME, "location-bar__dropdown-item-title")
	except (StaleElementReferenceException, TimeoutException):  # we are stuck
		continue;
	print("The number of locations we are pulling is: ", len(location_list))

	current_location = location_list[0]
	driver.execute_script("arguments[0].click();", current_location)  # enter current location

	facility_index +=1
	print("Facility Index: ", facility_index)
	print("Facility Index: ", len(facility_list))
	driver.refresh()

	#
	# # We need to scroll in our facility list:
	# if (facility_index + 1) % 5 == 0:
	# 	number_of_clicks += 1
	# 	print("I HAPPEPPEPENED")
	# number_of_clicks = 10

	print("numb_of_clicks is " , number_of_clicks)

	for i in range(0, number_of_clicks):
		print("button about to got clicked")
		try:
			driver.implicitly_wait(1)
			time.sleep(2)
			next_button = driver.find_elements(By.CLASS_NAME, "carousel__button")[1]
			driver.execute_script("arguments[0].click();", next_button)
		except IndexError:
			print("Not Found")
			continue;

	try:  # refresh our facilities to prevent stale element exception
		WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, "tile__img")))
		facility_list = driver.find_elements(By.CLASS_NAME, "tile__img")
	except TimeoutException:
		facility_index -= 1;  # redo the iteration
		continue;

	# Open our facility
	try:
		current_facility = facility_list[facility_index]
		driver.execute_script("arguments[0].click();", current_facility)
	except StaleElementReferenceException:
		facility_index -=1
		continue



	# Stores what all sports you can play at this facility

	# Setting up Loop 3
	range_of_loop3 = 1  # by default, we still loop once
	multiple_sport_flag = False;
	sport_options_list_2 = []
	try:
		WebDriverWait(driver, wait_time).until(
			EC.presence_of_element_located((By.CLASS_NAME, "sports-modal__sport-tile-title")))
		sport_options_list = driver.find_elements(By.CLASS_NAME, "sports-modal__sport-tile-title")

		for element in sport_options_list:
			sport_options_list_2.append(element.text)

		range_of_loop3 = len(sport_options_list)
		multiple_sport_flag = True;

	except TimeoutException:
		print("Element not found within the specified wait time using: ", "sports-modal__sport-tile-title")
		pass

	print("My sport_options_list looks like ", sport_options_list_2)
	range_of_loop3 = len(sport_options_list_2)
	# Loop 3: varying sports option clicking, this will still run one iteration even if we don't have multiple sports
	if range_of_loop3 > 1:
		multiple_sport_flag = True
	else:
		range_of_loop3 = 1
	for sport_index in range(0, range_of_loop3):
		print("My sport index is ", sport_index)
		if multiple_sport_flag:  # if we have multiple sports to click through
			if sport_index == 0:
				driver.refresh()
			else:
				driver.back()  # this means we have already clicked on a sport

			try:
				WebDriverWait(driver, wait_time).until(
					EC.presence_of_element_located((By.CLASS_NAME, "sports-modal__sport-tile-title")))
				sport_options_list = driver.find_elements(By.CLASS_NAME, "sports-modal__sport-tile-title")
				driver.execute_script("arguments[0].click();", sport_options_list[sport_index])

			except TimeoutException:
				print("2 Element not found within the specified wait time using: ",
				      "sports-modal__sport-tile-container")
				pass
		# We are here after we clicked a sport and are on the information page

		# PERFORM ALL ACTIONS
		# if len(sport_options) == 0:
		# 	sport_options.append("N/A")
		# sport_options = list(set(sport_options))
		# print("Sport Options: ", sport_options)

		# Wait for data to load
		try:
			WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, "header__title")))
		except TimeoutException:
			sport_index -=1
			print("RESET")
			continue
		# ACTION: Scrape information
		# Title
		facility_title = driver.find_element(By.CLASS_NAME, "header__title").text
		print("Facility Title: ", facility_title)

		# Location
		facility_location = driver.find_element(By.CLASS_NAME, "header__sub-title").text

		# Parse the location to get the specific elements
		# Splitting the address components
		parts = facility_location.split(',')

		facility_street_address = "N/A"
		facility_city = "N/A"
		facility_state = "N/A"
		facility_zip_code = "N/A"

		if len(parts) == 3:
			facility_street_address = parts[0].strip()
			facility_city = parts[1].strip()
			facility_state_zip = parts[2].strip().split()
			if len(facility_state_zip) == 2:
				facility_state = facility_state_zip[0]
				facility_zip_code = facility_state_zip[1]

		print("Facility Location: ", facility_location)
		print(f"Street Address: {facility_street_address}")
		print(f"City: {facility_city}")
		print(f"State: {facility_state}")
		print(f"Zip Code: {facility_zip_code}")

		# Image
		try:
			image_button = driver.find_element(By.CLASS_NAME, "photos-btn")
			driver.execute_script("arguments[0].click();", image_button)
			WebDriverWait(driver, wait_time).until(
				EC.presence_of_element_located((By.CLASS_NAME, "caption-text")))

			my_counter = 0
			text_image_array = []

			WebDriverWait(driver, wait_time).until(
				EC.presence_of_element_located((By.CLASS_NAME, "caption-text")))

			caption_text = driver.find_elements(By.CLASS_NAME, 'caption-text')

			carousel_items = driver.find_elements(By.CLASS_NAME, 'carousel-item')

			# Locate the caption text within the carousel-item
			caption_text_element = carousel_items[0].find_element(By.CSS_SELECTOR, '.caption-text')

			# Get the text from the caption element
			caption_text = caption_text_element.text
			image_list = []
			for carousel_item in carousel_items:
				print(carousel_item)
				style_attribute = carousel_item.get_attribute('style')
				current_image = re.search(r'url\("(.*?)"\)', style_attribute).group(1)
				image_list.append(current_image)

		# attempt to pulll the caption text, but it didn't work
		# for text in caption_text:
		# 	print("This is my: ", text.text)
		# while True:
		#
		# 	if my_counter >= 20:
		# 		print("DONE!")
		# 		break  # emergency break
		# 	try:
		# 		my_counter+=1
		# 		WebDriverWait(driver, wait_time).until(
		# 			EC.presence_of_element_located((By.CLASS_NAME, "caption-text")))
		# 		driver.implicitly_wait(3)
		#
		# 		caption_text = driver.find_element(By.CLASS_NAME, "caption-text").text
		# 		print("This is my 2: ", caption_text)
		#
		# 		next_button = driver.find_element(By.CLASS_NAME, "carousel-control-next-icon")
		#
		# 		driver.execute_script("arguments[0].click();", next_button)
		#
		# 		# Check if array is empty or if the first element of the new tuple
		# 		# doesn't match the first element of the last tuple in the array
		# 		# if len(text_image_array) >= 3 and text_image_array[-1][1] == text_image_tuple[1]:
		# 		# 	print("This is happening")
		# 		# 	print(text_image_array[-1][1])
		# 		# 	print(text_image_tuple[1])
		# 		# 	break
		# 	except TimeoutException:
		# 		facility_picture = "N/A"
		# 		break; ##a
		# facility_pictures = driver.find_element(By.CLASS_NAME, "img-responsive").get_attribute('src')
		except NoSuchElementException:
			facility_picture = "N/A"

		# printing my array:
		print(text_image_array)
		# Sport Update (if available) *MAY NEED TO USE NLP AND CLASSIFICATION*
		# --> derive from the title of the place
		if not multiple_sport_flag:  # we only need to classify if we don't have multiple sports, as
			# we only have one sport whose info isn't provided
			pass  # INSERT CODE

		# Declare the timings structure

		# Extract Price
		times_list = driver.find_elements(By.CLASS_NAME, "listing-tile")
		time_list_length = len(times_list)

		if time_list_length > 1:
			try:
				# Wait for data to load
				WebDriverWait(driver, wait_time).until(
					EC.presence_of_element_located((By.CLASS_NAME, "listing-tile__price")))

				price_list = driver.find_elements(By.CLASS_NAME, "listing-tile__price")
				new_price_list = []
				for price in price_list:
					price = price.text
					# Remove the dollar sign
					price = price.replace('$', '')
					# Convert to float
					print("OUR PRICE IS 1", price)
					try:
						price = float(price)
						print("OUR PRICE IS 2", price)
						new_price_list.append(price)
					except ValueError:
						continue
				if new_price_list:
					price = min(new_price_list)
				else:
					price = "N/A"
			except TimeoutException:
				price = "N/A"
				break;
		else:
			price = "N/A"

		# Extract the link
		current_url = driver.current_url

		# Print the extracted details
		print(f"Price: {price}")
		print(f"Link: {current_url}")
		print("-" * 40)

		print("This is happening rn ")

		if multiple_sport_flag:
			my_sport = sport_options_list_2[sport_index]
		else:
			match = re.search(r'sport=([^&]+)', current_url)
			if match:
				my_sport = match.group(1)
				print(f"The word after sport= is: {my_sport}")
			else:
				print("No sport parameter found.")
				my_sport = "N/A"
		print()
		add_to_csv(facility_title, facility_city, my_sport, facility_location,
		           facility_street_address, facility_zip_code,
		           "N/A", "N/A", image_list[0], image_list[0], image_list, price, "VARYING PRICES",
		           sport_options_list_2, current_url)

		# Loop 4: pull the timings and store
		if include_time_data:
			# Find all elements with the class name "listing-tile"
			times_list = driver.find_elements(By.CLASS_NAME, "listing-tile")

			time_index = 0
			time_list_length = len(times_list)
			time_refresh_flag = False  # if we need to keep waiting for our times to load
			year_flag = False  # this is for checking if we should add to the year
			# Loop through each element in the times_list to extract details
			# previous_month = ""
			time_counter_for_testing = 0
			while True:
				availability = {
					2024: {
						1: {day: [] for day in range(1, 32)},
						2: {day: [] for day in range(1, 30)},
						3: {day: [] for day in range(1, 32)},
						4: {day: [] for day in range(1, 31)},
						5: {day: [] for day in range(1, 32)},
						6: {day: [] for day in range(1, 31)},
						7: {day: [] for day in range(1, 32)},
						8: {day: [] for day in range(1, 32)},
						9: {day: [] for day in range(1, 31)},
						10: {day: [] for day in range(1, 32)},
						11: {day: [] for day in range(1, 31)},
						12: {day: [] for day in range(1, 32)}
					},
					2025: {
						1: {day: [] for day in range(1, 32)},
						2: {day: [] for day in range(1, 30)},
						3: {day: [] for day in range(1, 32)},
						4: {day: [] for day in range(1, 31)},
						5: {day: [] for day in range(1, 32)},
						6: {day: [] for day in range(1, 31)},
						7: {day: [] for day in range(1, 32)},
						8: {day: [] for day in range(1, 32)},
						9: {day: [] for day in range(1, 31)},
						10: {day: [] for day in range(1, 32)},
						11: {day: [] for day in range(1, 31)},
						12: {day: [] for day in range(1, 32)}
					},
				}

				time_counter_for_testing += 1
				if testing_number_of_times <= time_counter_for_testing:
					print("breaking here")
					break
				# #Set a date and time we want to pick
				# # #1) get our calendar and click it
				# # calendar_element = driver.find_element(By.CLASS_NAME, "calendar-icon")
				# #2)
				# days = driver.find_elements(By.CLASS_NAME, "mat-grid-tile-content")
				# day_index = 0
				# #within our days we need to click next to move onto a new page
				# #each page has two months so we can only do in multiples of 2
				# for day_index in (0, len(days)):
				# 	days = driver.find_elements(By.CLASS_NAME, "mat-grid-tile-content")
				# 	current_day = days[day_index]
				# 	print(current_day.text)

				# Redo list to prevent stale element exception
				try:
					# Wait for data to load
					WebDriverWait(driver, wait_time).until(
						EC.presence_of_element_located((By.CLASS_NAME, "listing-tile")))

					times_list = driver.find_elements(By.CLASS_NAME, "listing-tile")
					tile = times_list[time_index]
					time_list_length = len(times_list)
				except TimeoutException:
					print("I happened 1")
					break;

				# Extract time
				time_container = tile.find_element(By.CLASS_NAME, "listing-tile__time-container")
				current_time = time_container.find_element(By.CLASS_NAME, "listing-tile__time").text.strip()

				# Extract date
				date_container = tile.find_element(By.CLASS_NAME, "listing-tile__date-contianer")
				date_weekday = date_container.find_element(By.CLASS_NAME, "listing-tile__weekday").text
				date = date_container.find_element(By.CLASS_NAME, "listing-tile__date").text

				if date == "" or date is None:
					print("Breaking because of a lack of data getting")
					break
				# Add to our dictionary

				# Update our year correctly
				month = date.split()[0]

				if month == "Jan" and year_flag:
					current_year += 1
					year_flag = False

				if month != "Jan":  # that means if we encounter a year flag it has become a new year
					year_flag = True

				day = date.split()[1]

				# add_to_csv
				# add_to_csv(facility_id, facility_title, facility_location, facility_picture, current_url,
				#            sport_options_list_2[sport_index], current_year, month, day, current_time, price, csv_file)

				print("This is happening")

				# Update our dictionary
				update_availability_time_slot(current_year, month, day, current_time)

				# Locate the container element
				facility_listings_container = driver.find_element(By.ID, "facilityListingsContainer")

				# Scroll the container element by 400 pixels --> should be constant throughout all devices
				# POSSIBLE BOTTLENECK: varying scroll size
				scroll_script = """
				var container = arguments[0];
				container.scrollTop += 400;
				"""
				driver.execute_script(scroll_script, facility_listings_container)
				print(time_index, " ", time_list_length)
				if time_index >= time_list_length - 1:  # check if we have gone down by these many elements
					print("Here right now")
					time_refresh_flag = True

				# Sleep until we load in more times if there are any and our flag is set to true
				finish_counter = 0;
				if time_refresh_flag:
					while True:
						# Locate the container element
						facility_listings_container = driver.find_element(By.ID, "facilityListingsContainer")
						# driver.execute_script(scroll_script, facility_listings_container)
						og_time_list_length = time_list_length
						driver.implicitly_wait(0.1)
						times_list = driver.find_elements(By.CLASS_NAME, "listing-tile")
						time_list_length = len(times_list)
						if finish_counter >= 30 or og_time_list_length != time_list_length:
							time_refresh_flag = False
							break;
						finish_counter += 1
				print("The time_list_length = ", time_list_length)
				if time_index >= (time_list_length - 1):
					print("breaking here because of time index")
					break
				time_index += 1

	# ACTION: CSV / DB
	# We are sending our spreadsheet our: link, sport name, price, timings, image link

	# Go back a page and restart
	if multiple_sport_flag:  # Multiple sports to get past
		driver.back()
	driver.back()

	print("length of facility list: ", len(facility_list))
	if facility_index >= (len(facility_list) - 1):
		# Wait for the page to load the locations by clicking the dropdown
		click_after_wait("location-bar__text")
		print("I happened 2")

	if facility_index >= len(facility_list):
		break

# After we are done with our work we need to return back and retrieve our next location

# Click drop down button to prevent any location issues
# dropdown_button = driver.find_element(By.CLASS_NAME, "location-bar__dropdown-icon--up")
# driver.execute_script("arguments[0].click();", dropdown_button)

print("Done!")
driver.quit()
