import house_data
import pandas

first_url_start = "https://www.zoopla.co.uk/for-sale/houses"
base_url = "https://www.zoopla.co.uk"
df = pandas.DataFrame()

def search_website(city, min_price, max_price, min_beds, max_beds):
	global df
	city_1, city_2 = city_http(city)
	beds_max = max_beds_http(max_beds)
	beds_min = min_beds_http(min_beds, max_beds)
	price_max = max_price_http(max_price, min_beds, max_beds)
	price_min = min_price_http(min_price, max_price, min_beds, max_beds)
	extra = extra_http(min_price, max_price, min_beds, max_beds)

	first_url = first_url_start + city_1 + beds_max + beds_min + price_max + price_min + extra + city_2
	df = house_data.get_data(base_url, first_url)
	return df.size
	
def save_file(df):
	house_data.save_csv(df)

def get_df():
	return df

def city_http(city):
	if city == "Birmingham":
		city_1 = "/birmingham/?"
		city_2 = "q=birmingham&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Brighton":
		city_1 = "/east-sussex/brighton/?"
		city_2 = "q=brighton&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Bristol":
		city_1 = "/bristol/?"
		city_2 = "q=bristol&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Coventry":
		city_1 = "/coventry/?"
		city_2 = "q=coventry&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Lancaster":
		city_1 = "/lancaster/?"
		city_2 = "q=lancaster&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Leeds":
		city_1 = "/leeds/?"
		city_2 = "q=leeds&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Leicester":
		city_1 = "/leicester/?"
		city_2 = "q=leicester&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Liverpool":
		city_1 = "/liverpool/?"
		city_2 = "q=liverpool&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "London-East":
		city_1 = "/east-london/?"
		city_2 = "q=east%20london&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "London-North":
		city_1 = "/north-london/?"
		city_2 = "q=north%20london&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "London-South":
		city_1 = "/south-london/?"
		city_2 = "q=south%20london&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "London-West":
		city_1 = "/west-london/?"
		city_2 = "q=west%20london&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Manchester":
		city_1 = "/manchester/?"
		city_2 = "q=Manchester&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Newcastle":
		city_1 = "/newcastle-upon-tyne/?"
		city_2 = "q=Newcastle%20upon%20Tyne%2C%20Tyne%20%26%20Wear&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Norwich":
		city_1 = "/norwich/?"
		city_2 = "q=Norwich&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Nottingham":
		city_1 = "/nottingham/?"
		city_2 = "q=nottingham&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Portsmouth":
		city_1 = "/portsmouth/?"
		city_2 = "q=portsmouth&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Southampton":
		city_1 = "/southampton/?"
		city_2 = "q=southampton&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "Stoke":
		city_1 = "/stoke-on-trent/?"
		city_2 = "q=Stoke-on-Trent%2C%20Staffordshire&radius=0&results_sort=lowest_price&search_source=refine"
	elif city == "York":
		city_1 = "/york/?"
		city_2 = "q=york&radius=0&results_sort=lowest_price&search_source=refine"
	return (city_1, city_2)

def min_price_http(min_price, max_price, min_beds, max_beds):
	if min_price == "":
		minimum_price = ""
	elif min_beds == "" and max_beds == "" and max_price == "":
		minimum_price = f"price_min={min_price}"
	else:
		minimum_price = f"&price_min={min_price}"
	return minimum_price

def max_price_http(max_price, min_beds, max_beds):
	if max_price == "":
		maximum_price = ""
	elif min_beds == "" and max_beds == "":
		maximum_price = f"price_max={max_price}"
	else:
		maximum_price = f"&price_max={max_price}"
	return maximum_price

def min_beds_http(min_beds, max_beds):
	if min_beds == "":
		minimum_beds = ""
	elif max_beds == "":
		minimum_beds = f"beds_min={min_beds}"
	else:
		minimum_beds = f"&beds_min={min_beds}"
	return minimum_beds

def max_beds_http(max_beds):
	if max_beds == "":
		maximum_beds = ""
	else:
		maximum_beds = f"beds_max={max_beds}"
	return maximum_beds

def extra_http(min_price, max_price, min_beds, max_beds):
	if min_price == "" and max_price == "" and min_beds == "" and max_beds == "":
		extra = ""
	else:
		extra = "&"
	return extra
	