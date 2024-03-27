#!/usr/bin/env python3 
# jorune00 - jorune.dev -- 2023-11-21 11:34:24
# Generate XML file with holiday dates for UCCX phone system
# No leading zeros on dates - 1/1/2024 instead of 01/01/2024

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

# Function to find the date of Easter Sunday for a given year
def find_easter(year):
    # Calculate the date of Easter Sunday using the Anonymous Gregorian algorithm
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    easter = datetime.date(year, month, day)
    return easter

# Function to find the date of Good Friday for a given year
def find_good_friday(year):
    # Good Friday is the Friday before Easter Sunday
    # Start with Easter Sunday
    easter = find_easter(year)
    good_friday = easter - datetime.timedelta(days=2)
    return good_friday

# Define the start year and the number of years
start_year = 2024
num_years = 8

# Create the root element
holidays = ET.Element("Holidays")

# Counter for holiday numbering
holiday_counter = 1

# Loop to add holidays for each year
for i in range(num_years):
    year = start_year + i

    # Add New Year's Day holiday
    jan1 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    jan1.text = f"1/1/{year}"
    holiday_counter += 1

    # Add Good Friday holiday
    good_friday = find_good_friday(year)
    good_friday_element = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    good_friday_element.text = good_friday.strftime("%-m/%-d/%Y")
    holiday_counter += 1

    # Add Memorial Day holiday
    memorial_day = find_memorial_day(year)
    memorial = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    memorial.text = memorial_day.strftime("%-m/%-d/%Y")
    holiday_counter += 1

    # Add July 4th holiday
    july4 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    july4.text = f"7/4/{year}"
    holiday_counter += 1

    # Add Labor Day holiday
    labor_day = find_labor_day(year)
    labor = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    labor.text = labor_day.strftime("%-m/%-d/%Y")
    holiday_counter += 1

    # Add Thanksgiving
    thanksgiving_date = find_thanksgiving(year)
    thanksgiving = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    thanksgiving.text = thanksgiving_date.strftime("%-m/%-d/%Y")
    # thanksgiving.text = f"{thanksgiving_date.month}/{thanksgiving_date.day}/{thanksgiving_date.year}"
    # possibly use the above line to format the date if needed - instead of thanksgiving.text = thanksgiving_date.strftime("%-m/%-d/%Y")
    holiday_counter += 1

    # Add day after Thanksgiving
    thanksgiving_friday = thanksgiving_date + datetime.timedelta(days=1)
    thanksgiving_friday_element = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    thanksgiving_friday_element.text = thanksgiving_friday.strftime("%-m/%-d/%Y")
    holiday_counter += 1

# TODO: Removed Christmas Eve and New Year's Eve holidays for now
    # # Add Christmas Eve holiday
    # dec24 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    # dec24.text = f"12/24/{year}"
    # holiday_counter += 1

    # Add December 25th holiday
    dec25 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    dec25.text = f"12/25/{year}"
    holiday_counter += 1

# TODO: Removed Christmas Eve and New Year's Eve holidays for now
    # # Add New Year's Eve holiday
    # dec31 = ET.SubElement(holidays, f"Holiday{holiday_counter}")
    # dec31.text = f"12/31/{year}"
    # holiday_counter += 1

# Create a rough string from the ElementTree
rough_string = ET.tostring(holidays, 'utf-8')

# Use minidom to prettify without adding a declaration
reparsed = minidom.parseString(rough_string)
pretty_string = reparsed.toprettyxml(indent="  ")

# Remove the automatically added declaration from minidom
pretty_string_without_declaration = '\n'.join(pretty_string.split('\n')[1:])

# Write to file with custom XML declaration
with open("dates_v2.xml", "w", encoding='ISO-8859-1') as file:
    file.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
    file.write('<!-- NO LEADING ZEROES IN DATE NUMBERS !!!! -->\n')
    file.write('<!-- Generated by Date_Generator.py -->\n')
    file.write('<!-- jorune00 - jorune.dev - jheintz@fp-usa.com -->\n')
    file.write(pretty_string_without_declaration)
