#!/usr/bin/env python 
# jorune00 - jorune.dev -- 2023-11-21 11:34:24

import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime

# Function to find the date of Thanksgiving for a given year
def find_thanksgiving(year):
    # Find the fourth Thursday of November
    date = datetime.date(year, 11, 1)
    # Count how many days to the first Thursday
    days_to_thursday = 3 - date.weekday()
    if days_to_thursday < 0:
        days_to_thursday += 7
    # Add three weeks (21 days) to get to the fourth Thursday
    thanksgiving = date + datetime.timedelta(days=days_to_thursday + 21)
    return thanksgiving

# Function to find the date of Memorial Day for a given year
def find_memorial_day(year):
    # Memorial Day is the last Monday in May
    # Start with the last day of May
    date = datetime.date(year, 5, 31)
    # Count backwards to the nearest Monday
    days_to_monday = date.weekday()
    memorial_day = date - datetime.timedelta(days=days_to_monday)
    return memorial_day

# Function to find the date of Labor Day for a given year
def find_labor_day(year):
    # Labor Day is the first Monday in September
    # Start with the first day of September
    date = datetime.date(year, 9, 1)
    # Count how many days to the first Monday
    days_to_monday = 0 if date.weekday() == 0 else 7 - date.weekday()
    labor_day = date + datetime.timedelta(days=days_to_monday)
    return labor_day

# Define the start year and the number of years
start_year = 2024
num_years = 5

# Create the root element
holidays = ET.Element("Holidays")

# Counter for holiday numbering
holiday_counter = 1

# Loop to add holidays for each year
for i in range(num_years):
    year = start_year + i

    # Add Memorial Day holiday
    memorial_day = find_memorial_day(year)
    memorial = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    memorial.text = memorial_day.strftime("%m/%d/%Y")
    holiday_counter += 1

    # Add July 4th holiday
    july4 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    july4.text = f"7/4/{year}"
    holiday_counter += 1

    # Add Labor Day holiday
    labor_day = find_labor_day(year)
    labor = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    labor.text = labor_day.strftime("%m/%d/%Y")
    holiday_counter += 1

    # Add Thanksgiving
    thanksgiving_date = find_thanksgiving(year)
    thanksgiving = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    thanksgiving.text = thanksgiving_date.strftime("%m/%d/%Y")
    holiday_counter += 1

    # Add Christmas Eve holiday
    dec24 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    dec24.text = f"12/24/{year}"
    holiday_counter += 1

    # Add December 25th holiday
    dec25 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    dec25.text = f"12/25/{year}"
    holiday_counter += 1

    # Add New Year's Eve holiday
    dec31 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    dec31.text = f"12/31/{year}"
    holiday_counter += 1

    # Add New Year's Day holiday
    jan1 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    jan1.text = f"1/1/{year}"
    holiday_counter += 1

# Create a rough string from the ElementTree
rough_string = ET.tostring(holidays, 'utf-8')

# Use minidom to prettify without adding a declaration
reparsed = minidom.parseString(rough_string)
pretty_string = reparsed.toprettyxml(indent="  ")

# Remove the automatically added declaration from minidom
pretty_string_without_declaration = '\n'.join(pretty_string.split('\n')[1:])

# Write to file with custom XML declaration
with open("dates.xml", "w", encoding='ISO-8859-1') as file:
    file.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    file.write(pretty_string_without_declaration)