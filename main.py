import pandas
import json
import openpyxl
from datetime import datetime

# NOTE: THIS SOLUTION ASSUMES THE FILE IS IN THE PROJECT DIRECTORY

# Display all columns and rows
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_rows', None)

# Error handling for file reading and DataFrame processing
try:
    # Reading xlsx file and removing the NaN values
    menuDF = pandas.read_excel("Mess Menu Sample.xlsx").fillna('')
    # print(menuDF) [debugging]

except Exception as e:
    print(f"Error reading the Excel file: {e}")
    exit(1)

# Converting DataFrame to dictionary
try:
    menu_dict = menuDF.to_dict()
    # print(menu_dict) [debugging]
except Exception as e:
    print(f"Error converting DataFrame to dictionary: {e}")
    exit(1)

# Removing the day names as required, we will use only dates and the names of meals and dishes
menu = list(menu_dict.values())
# print(menu) #for debugging

menu_by_date = []
# Processing menu data
for item in menu:
    start_key = 1
    end_key = len(item) - 1
    result = []

    for key, value in item.items():
        if start_key <= key <= end_key and isinstance(value, str):
            result.append(value.strip())

    menu_by_date.append({item[0]: result})
# print(menu_by_date) [debugging]


# SEPARATING DISHES INTO SPECIFIC MEALS

# Defining days (they will act as point of separation to separate dishes)
days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

# Dividing meals into breakfast, lunch, and dinner
for menu_dict in menu_by_date:  # get hold of a dictionary from the list with date as key and entire daily menu as value
    for key, value in menu_dict.items():  # get hold of the date and daily menu
        i = 0
        # lists to store meal dishes
        breakfast = []
        lunch = []
        dinner = []

        # LOGIC FOR EXTRACTING MEALS: MEALS ARE SEPARATED BY THE NAME OF THE DAY (MONDAY, TUESDAY ETC...)
        # AND BREAKFAST COMES FIRST, FOLLOWED BY LUNCH AND DINNER

        # Extract breakfast dishes
        while i < len(value) and value[i] not in days:
            if isinstance(value[i], str) and '*' not in value[i]:  # pick string and avoid **** error values
                breakfast.append(value[i].strip())  # remove white space
            i += 1
        if i < len(value):
            i += 1  # Skipping the day name

        # Extract lunch
        while i < len(value) and value[i] not in days:
            if isinstance(value[i], str) and '*' not in value[i]:   # pick string and avoid **** error values
                lunch.append(value[i].strip())     # remove white space
            i += 1
        if i < len(value):
            i += 1  # Skipping the day name

        # Extracting dinner
        while i < len(value) and value[i] not in days:
            if isinstance(value[i], str) and '*' not in value[i]:   # pick string and avoid **** error values
                dinner.append(value[i].strip()) # remove white space
            i += 1
        if i < len(value):
            i += 1  # Skipping the day name


        # Storing dishes in meals which they belong to
        meals_dict = {
            "BREAKFAST": breakfast[1:],  # Removed first element which could be an empty value
            "LUNCH": lunch[1:],          # Removed first element which could be an empty value
            "DINNER": dinner[1:]         # Removed first element which could be an empty value
        }

        # Updating the meals with respective dishes in menu_by_dates
        menu_dict[key] = meals_dict

# PROCESSING DATE
updated_menu_by_date = {}

for daily_menu in menu_by_date:
    try:
        date_object = list(daily_menu.keys())[0]  # Extract the first key (datetime object)

        # Then we extract year, month, and date to create date in the required format
        year = date_object.year
        month = str(date_object.month).zfill(2)
        day = str(date_object.day).zfill(2)

        # Create the new menu with correctly formatted dates
        updated_menu_by_date[f"{year}-{month}-{day}"] = daily_menu[date_object]

    except Exception as e:
        print(f"Error processing date for {daily_menu}: {e}")
        continue

# Writing to JSON with error handling
try:
    with open("mess_menu.json", "w") as JSON_FILE:
        JSON_FILE.write(json.dumps(updated_menu_by_date, indent=3))
except Exception as e:
    print(f"Error writing to JSON file: {e}")
    exit(1)
