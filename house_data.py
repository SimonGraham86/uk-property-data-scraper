import requests
from bs4 import BeautifulSoup
import pandas
from house_class import House
import os


#This function gets a list of properties and adds them to a pandas DataFrame.
#The df is returned.
def get_data(base_url, first_url):
	results = iter_pages(base_url, first_url)
	df = pandas.DataFrame(results, columns =
		["Address"
		,"Post Code"
		,"Beds"
		,"Baths"
		,"Recepetion Rooms"
		,"Price"
		,"Nearest Station"
		,"Distance to Station"])
	return df

#This function saves the pandas DataFrame as a CSV file in the user's Downloads folder.
def save_csv(df):
	home = os.path.expanduser("~")
	file_name = os.path.join(home, "Downloads\\Houses.csv")
	df.to_csv(file_name, index=False)

#----------------------------------------------------------------------------------------------------------------------------------------------------

###############
# Data Scrape #
###############

#This function will start with an empty results_list.
#It will iterate through all of the webpages, gathering information from each property on every page.
#Once a page has been completed, this will be printed in the command prompt window.
#The function will end once the final page has been completed and will return a completed results_list.
def iter_pages(base_url, first_url):
	results_list = []
	next_http = None
	page = 1

	while True:
		soup = get_soup(base_url, first_url, next_http, page)
		items = items_to_search(soup)
		results_list = iter_results(items, results_list)

		if check_next(next_http,soup) == False:
			print("Finished Page " + str(page))
			break
		else:
			next_http = next_page(next_http, soup)
		print("Finished Page " + str(page))
		page += 1

	return results_list

#This function will iterate through the individual items in the list of properties.
#It will gather the information for each item and then create a House class object for the item.
#The House object will then be addes to the results_list.
#Once all items have been iterated through, the updated results_list will be returned.
def iter_results(items, results_list):
	for item in items:
		address = get_address(item)
		postcode = get_postcode(item)
		beds = get_beds(item)
		baths = get_baths(item)
		recs = get_recs(item)
		price = get_price(item)
		station = get_near_stat(item)
		distance = get_stat_dist(item)
		house = House(address, postcode, beds, baths, recs, price, station, distance)
		results_list.append(house.house_details())
	return results_list

#This function goes through all of the html for an individual webpage.
#It then breaks them up into a list of individual items (properties).
#If there are no items on the page, it will return an empty list.
def items_to_search(soup):
	try:
		items = soup.find("ul", {"class":"listing-results"}).find_all("div", {"class":"listing-results-right clearfix"})
	except:
		items = []
	return items

#This function gets the html content from the individual pages.
#If it is the first page, it will use the 'first_url' argument, otherwise it will use 'base_url + next_http'.
#It will return the html.	
def get_soup(base_url, first_url, next_http, page):
	if page == 1:
		r = requests.get(first_url)
	else:
		r = requests.get(base_url + next_http)
	c = r.content
	soup = BeautifulSoup(c, "html.parser")
	return soup

#----------------------------------------------------------------------------------------------------------------------------------------------------

#############
# NEXT PAGE #
#############

#This function uses the next_page() function to check whether or not there is a next page.
#If next_page() returns a different http, it will return True, otherwise it will return False.
def check_next(next_http, soup):
    next_search_check = next_http
    next_http = next_page(next_http, soup)
    if next_http == next_search_check:
        return False
    else:
    	return True

#This function checks to see if there is a 'Next' link in the paginate section of the webpage.
#If there is one, the link to the next page will be returned. 
#If not, the 'next_http' argument from the function will be returned.
def next_page(next_http, soup):
	try:
		page_links = soup.find("div",{"class":"paginate"}).find_all("a")
	except:
		page_links = []
	for link in page_links:
		if link.text == "Next":
			next_http = link["href"]
	return next_http

#----------------------------------------------------------------------------------------------------------------------------------------------------

##############
# ATTRIBUTES #
##############

#Finds the address for the individual property or returns None
def get_address(item):
	try:
		address = item.find("a", {"class":"listing-results-address"}).text
		address2 = address.split()
		myaddress = " ".join(address2[:-1])
	except:
		myaddress = None
	return myaddress

#Finds the postcode for the individual property or returns None
def get_postcode(item):
	try:
		address = item.find("a", {"class":"listing-results-address"}).text
		address2 = address.split()
		postcode = address2[-1]
	except: 
		postcode = None
	return postcode

#Finds the no. of bedrooms for the individual property or returns None
def get_beds(item):
	try:
		beds = item.find("span", {"class":"num-beds"}).text
	except: 
		beds = None
	return beds

#Finds the no. of bathrooms for the individual property or returns None
def get_baths(item):
	try:
		baths = item.find("span", {"class":"num-baths"}).text
	except: 
		baths = None
	return baths

#Finds the no. of reception rooms for the individual property or returns None
def get_recs(item):
	try:
		recs = item.find("span", {"class":"num-reception"}).text
	except: 
		recs = None
	return recs

#Finds the price for the individual property or returns None
def get_price(item):
	try:
		price = item.find("a", {"class":"listing-results-price"}).text.replace("\n","")
		house_price = price.split()[0]
	except:
		house_price = None
	return house_price

#Finds the nearest station for the individual property or returns None
def get_near_stat(item):
	try:
		station = item.find("span", {"class":"nearby_stations_schools_name"}).text
	except:
		station = None
	return station

#Finds the distance to the nearest station for the individual property or returns None
def get_stat_dist(item):
	try:
		distance = item.find("li", {"class":"clearfix"})
		distance.span.decompose()
		distance.span.decompose()
		stat_dist = distance.text.replace("\n","").replace(" (","").replace(")","")
	except:
		stat_dist = None
	return stat_dist