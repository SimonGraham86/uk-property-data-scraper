class House:

	def __init__(self, address, post_code, beds, baths, recs, price, near_stat, distance):
		self.address = address
		self.post_code = post_code
		self.beds = beds
		self.baths = baths
		self.recs = recs
		self.price = price
		self.near_stat = near_stat
		self.distance = distance

	def house_details(self):
		house = [self.address, self.post_code, self.beds, self.baths, self.recs, self.price, self.near_stat, self.distance]
		return house

		