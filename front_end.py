from tkinter import *
from tkinter import messagebox
import back_end as be

class Window():
	def __init__(self, window):
		self.window = window
		self.window.wm_title("House Search")
		self.window.state("zoomed")

		#Lists for dropdown lists
		self.options_city = ["Birmingham","Brighton","Bristol","Coventry","Lancaster","Leeds","Leicester","Liverpool","London-East","London-North","London-South","London-West","Manchester","Newcastle","Norwich","Nottingham","Portsmouth","Southampton","Stoke","York"]
		mylist = []
		for i in range(0, 1000001, 25000):
			mylist.append(str(i))
		self.options_price = mylist
		self.options_beds = ["1","2","3","4","5"]

		#title
		title = Label(window, text="House Search", font="arial 30 bold", fg="white", bg="blue")
		title.grid(row=1, column=1, columnspan=2, sticky="nsew")

		#labels
		label_city = Label(master=window, text="Choose City:", font="arial 18", fg="white", bg="blue")
		label_city.grid(row=3, column=1, sticky="nse", padx=10)
		label_min_price = Label(master=window, text="Min Price:", font="arial 18", fg="white", bg="blue")
		label_min_price.grid(row=4, column=1, sticky="nse", padx=10)
		label_max_price = Label(master=window, text="Max Price:", font="arial 18", fg="white", bg="blue")
		label_max_price.grid(row=5, column=1, sticky="nse", padx=10)
		label_min_beds = Label(master=window, text="Min Beds:", font="arial 18", fg="white", bg="blue")
		label_min_beds.grid(row=6, column=1, sticky="nse", padx=10)
		label_max_beds = Label(master=window, text="Max Beds:", font="arial 18", fg="white", bg="blue")
		label_max_beds.grid(row=7, column=1, sticky="nse", padx=10)
		label_message = Label(window, text="Please Fill Out The Form", font="arial 12", fg="white", bg="blue")
		label_message.grid(row=9, column=1, columnspan=2, sticky="nsew", padx=10)

		#drop down lists
		self.choice_city = StringVar()
		self.list_city = OptionMenu(window, self.choice_city, *self.options_city)
		self.list_city.configure(width=10, bg="white", fg="blue", font="arial 12")
		self.list_city.grid(row=3, column=2, sticky="nsw", padx=10)

		self.choice_min_price = StringVar()
		self.list__min_price = OptionMenu(window, self.choice_min_price, *self.options_price)
		self.list__min_price.configure(width=10, bg="white", fg="blue", font="arial 12")
		self.list__min_price.grid(row=4, column=2, sticky="nsw", padx=10)		

		self.choice_max_price = StringVar()
		self.list__max_price = OptionMenu(window, self.choice_max_price, *self.options_price)
		self.list__max_price.configure(width=10, bg="white", fg="blue", font="arial 12")
		self.list__max_price.grid(row=5, column=2, sticky="nsw", padx=10)		

		self.choice_min_beds = StringVar()
		self.list__min_beds = OptionMenu(window, self.choice_min_beds, *self.options_beds)
		self.list__min_beds.configure(width=10, bg="white", fg="blue", font="arial 12")
		self.list__min_beds.grid(row=6, column=2, sticky="nsw", padx=10)		

		self.choice_max_beds = StringVar()
		self.list__max_beds = OptionMenu(window, self.choice_max_beds, *self.options_beds)
		self.list__max_beds.configure(width=10, bg="white", fg="blue", font="arial 12")
		self.list__max_beds.grid(row=7, column=2, sticky="nsw", padx=10)

		#buttons
		self.button_get_data = Button(window, text="Search Houses", font="arial 12 bold", bg="white", fg="blue", command=self.search_command)
		self.button_get_data.grid(row=11, column=1, columnspan=2, sticky="nsew")
		self.button_download = Button(window, text="Download CSV File", font="arial 12 bold", bg="white", fg="blue", command=self.download_command)	
		self.button_download.grid(row=13, column=1, columnspan=2, sticky="nsew")
		self.button_quit = Button(window, text="Quit", font="arial 12 bold", bg="white", fg="blue", command=window.destroy)	
		self.button_quit.grid(row=15, column=1, columnspan=2, sticky="nsew")

		#border
		window.columnconfigure(0, minsize=100, weight=1)
		window.columnconfigure(3, minsize=100, weight=1)
		window.rowconfigure(0, minsize=100, weight=1)
		window.rowconfigure(16, minsize=100, weight=1)
		window.rowconfigure(2, minsize=20, weight=1)
		window.rowconfigure(8, minsize=20, weight=1)
		window.rowconfigure(10, minsize=20, weight=1)
		window.rowconfigure(12, minsize=15, weight=1)
		window.rowconfigure(14, minsize=15, weight=1)
		
		#window
		window.configure(bg = "blue")

	def search_command(self):
		if self.choice_city.get() == "":
			messagebox.showinfo("Information","Please Choose A City.")
		elif self.choice_min_price.get() != "" and self.choice_max_price.get() != "" and int(self.choice_min_price.get()) > int(self.choice_max_price.get()):
			messagebox.showinfo("Information","The Minimum Price Is More Than The Maximum Price.")
		elif self.choice_min_beds.get() != "" and self.choice_max_beds.get() != "" and int(self.choice_min_beds.get()) > int(self.choice_max_beds.get()):
				messagebox.showinfo("Information","The Minimum Beds Is More Than The Maximum Beds.")
		else:
			if messagebox.askyesno("Information","About to extract data.\n\nDo you want to continue?"):
				df_size = be.search_website(self.choice_city.get(), self.choice_min_price.get(), self.choice_max_price.get(), self.choice_min_beds.get(), self.choice_max_beds.get())
				self.check_zero_results(df_size)

	def download_command(self):
		houses_df = be.get_df()
		if houses_df.empty:
			messagebox.showinfo("Information","Error! Please Make Sure You Have Searched For Results!")
		else:
			be.save_file(houses_df)
			messagebox.showinfo("Information","CSV File Has Been Saved To The Downloads Folder.")

	def check_zero_results(self, df_size):
		try:
			df_size = df_size / 8
		except:
			df_size = 0
		if df_size == 0:
			messagebox.showinfo("Information","0 Results Found. Please Try Another Search")
		else:
			messagebox.showinfo("Information","Data Extracted.")

window = Tk()
Window(window)
window.mainloop()