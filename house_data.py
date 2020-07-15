import requests
from bs4 import BeautifulSoup
import pandas
from house_class import House
import os


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
def save_csv(df):
	home = os.path.expanduser("~")
	file_name = os.path.join(home, "Downloads\\Houses.csv")
	df.to_csv(file_name, index=False)

###############
# Data Scrape #
###############
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
def items_to_search(soup):
	try:
		items = soup.find("ul", {"class":"listing-results"}).find_all("div", {"class":"listing-results-right clearfix"})
	except:
		items = []
	return items
def get_soup(base_url, first_url, next_http, page):
	if page == 1:
		r = requests.get(first_url)
	else:
		r = requests.get(base_url + next_http)
	c = r.content
	soup = BeautifulSoup(c, "html.parser")
	return soup

#############
# NEXT PAGE #
#############
def check_next(next_http, soup):
    next_search_check = next_http
    next_http = next_page(next_http, soup)
    if next_http == next_search_check:
        return False
    else:
    	return True
def next_page(next_http, soup):
	try:
		page_links = soup.find("div",{"class":"paginate"}).find_all("a")
	except:
		page_links = []
	for link in page_links:
		if link.text == "Next":
			next_http = link["href"]
	return next_http

##############
# ATTRIBUTES #
##############
def get_address(item):
	try:
		address = item.find("a", {"class":"listing-results-address"}).text
		address2 = address.split()
		myaddress = " ".join(address2[:-1])
	except:
		myaddress = None
	return myaddress
def get_postcode(item):
	try:
		address = item.find("a", {"class":"listing-results-address"}).text
		address2 = address.split()
		postcode = address2[-1]
	except: 
		postcode = None
	return postcode
def get_beds(item):
	try:
		beds = item.find("span", {"class":"num-beds"}).text
	except: 
		beds = None
	return beds
def get_baths(item):
	try:
		baths = item.find("span", {"class":"num-baths"}).text
	except: 
		baths = None
	return baths
def get_recs(item):
	try:
		recs = item.find("span", {"class":"num-reception"}).text
	except: 
		recs = None
	return recs
def get_price(item):
	try:
		price = item.find("a", {"class":"listing-results-price"}).text.replace("\n","")
		house_price = price.split()[0]
	except:
		house_price = None
	return house_price
def get_near_stat(item):
	try:
		station = item.find("span", {"class":"nearby_stations_schools_name"}).text
	except:
		station = None
	return station
def get_stat_dist(item):
	try:
		distance = item.find("li", {"class":"clearfix"})
		distance.span.decompose()
		distance.span.decompose()
		stat_dist = distance.text.replace("\n","").replace(" (","").replace(")","")
	except:
		stat_dist = None
	return stat_dist