# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:42:27 2019

@author: clairebissett
"""

# TravelNest Project

import requests  # for HTTP requests
from bs4 import BeautifulSoup  # for scraping data
import pandas as pd  # for creating dataframe

# List of desired urls
url_list = [
    "https://www.airbnb.co.uk/rooms/14531512?s=51",
    "https://www.airbnb.co.uk/rooms/19278160?s=51",
    "https://www.airbnb.co.uk/rooms/1939240?s=51"
    ]
# Create dictionary to hold data
d = {
    "Property Name": [],
    "Property Type": [],
    "No. of Bedrooms": [],
    "No. of Bathrooms": [],
    "List of Amenities": []
    }


# Define a function to scrape necessary data from chosen url
def scraper(url, d):

    if isinstance(url, str):
        get_response = requests.get(url, timeout=10)  # variable containing result of GET request for chosen url

        soup = BeautifulSoup(get_response.text, 'html.parser')  # variable containing parsed, text version of HTML from url

        prop_name = soup.find("span", class_="_18hrqvin").text  # finds text from <span> element
        d["Property Name"].append(str(prop_name))  # adds Property Name to dictionary d

        info = soup.find("div", class_="_n5lh69r")  # finds <div> element with specified class

        prop_type_info = info.find("div", class_="_1p3joamp").text  # finds <div> element in variable info
        __, __, prop_type = str(prop_type_info).partition(' ')  # partitions string to isolate Property Type
        d["Property Type"].append(prop_type)  # adds Property Type to dictionary d

        bed_bath_info = info.find_all(class_="_czm8crp")

        bedrooms_info = bed_bath_info[2].text  # finds bedroom info text from list bed_bath_info
        bedrooms, __, __ = str(bedrooms_info).partition(' ')  # partitions string to isolate Number of Bedrooms
        d["No. of Bedrooms"].append(int(bedrooms))  # adds integer No. of Bedrooms to dictionary d

        bathrooms_info = bed_bath_info[3].text  # finds bathroom info text from list bed_bath_info  
        bathrooms, __, __ = str(bathrooms_info).partition(' ')  # partitions string to isolate Number of Bathrooms
        d["No. of Bathrooms"].append(int(bathrooms))  # adds integer No. of Bathrooms to dictionary d

        # Not all amenities are found, I attempted to use chromedriver and then BeutifulSoup to obtain a list
        # of all the amenities, however was not able to fully implement this.
        # I thought it better to provide a solution that was fully functional and which contained at least
        # a snapshot of the property's amenities as below.
        amenities_info = soup.find(id="amenities").find_all("div", class_="_czm8crp")  # finds amentities info
        amenities = []  # creates empty list to store amenities
        for i in range(0,4):
            amenities.append(str(amenities_info[i].text))  # adds each amenity (as string) to the list
        d["List of Amenities"].append(str(amenities).strip("[]"))  # adds string of Amenities to dictionary d
        
        return d

    else:
        return "Error: This is not a valid url"


# Loop through list of urls and scrapes data from each
for url in url_list:
    scraper(url, d)

df = pd.DataFrame(data=d)  # create a dataframe object from dicitonary d
print df  # display dataframe
