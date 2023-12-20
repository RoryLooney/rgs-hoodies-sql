import tkinter as tk
import re as re
import sqlite3

class Hoodies(tk.Frame):

    def __init__(self, parent, ):

        tk.Frame.__init__(self, bg="light blue", height=30, width=30)
        self.price = None
        self.grid(row=0, column=0)
        self.parent = parent

        self.tutor_groups = ["14-1", "14-2", "14-3", "14-4", "14-5", "14-6", "14-7", "14-8", ]
        self.sizes = {
            "pick a size": 0,
            "S": 17,
            "M": 19,
            "L": 21,
            "XL": 22,
        }
        self.possible_filters = {
            "order id": 0,
            "forename": 1,
            "surname": 2,
            "mobile number": 4,
            "date": 5,
            "tutor group": 3,
            "colour": 6,
            "size": 7,
            "quantity": 9,
            "price": 8
        }

        self.colours = ["red", "green", "indigo", "turquoise", "neon_yellow", "neon_pink", "old_highlighter"]

        self.intialise_variables()

        self.date_pattern = re.compile("\d{2}/\d{2}/\d{2}")

        self.create_database()

        # widigts unrealated to creating or searching through orders

        self.input_order_details = tk.Frame(self, bg="light blue", bd=3)
        self.input_order_details.grid(row=2, column=0, rowspan=5)

        self.order_details_search = tk.Frame(self, bg="orange", bd=3)
        self.order_details_search.grid(row=2, column=0, sticky="n")

        self.title = tk.Label(self, text="RGS Hoodie", bg="light blue")
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.switch_to_input = tk.Button(self, text="Input Order", command=lambda: self.tab_switcher(1))
        self.switch_to_search = tk.Button(self, text="Search Order", command=lambda: self.tab_switcher(2))

        self.switch_to_input.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.switch_to_search.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.clear_button = tk.Button(self, text="Clear Screen:", command=lambda: self.clear_screen(self.tab))
        self.clear_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.tab_switcher(1)

    def create_database(self):
        conn = sqlite3.connect('hoodies.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hoodie (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                forename TEXT NOT NULL,
                surname TEXT NOT NULL,
                mobile TEXT NOT NULL,
                date TEXT NOT NULL,
                tutor TEXT NOT NULL,
                colour TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price INTEGER NOT NULL 
            )
        ''')
        conn.commit()
        conn.close()

    def tab_switcher(self, tab):

        self.intialise_variables()

        if tab == 1:
            self.order_details_search.destroy()
            self.open_order_inputs()
        if tab == 2:
            self.input_order_details.destroy()
            self.open_order_search()

    def open_order_inputs(self):

        # widgits about creating an order

        self.intialise_variables()

        self.tab = 1

        self.input_order_details = tk.Frame(self, bg="orange", borderwidth=10, relief="ridge")
        self.input_order_details.grid(row=2, column=0, rowspan=5, columnspan=5, padx=15, pady=15)

        self.forename = tk.Label(self.input_order_details, text="Forename:", bg="orange")
        self.surname = tk.Label(self.input_order_details, text="Surname:", bg="orange")
        self.mobile = tk.Label(self.input_order_details, text="Mobile number:", bg="orange")
        self.date_label = tk.Label(self.input_order_details, text="Date, Format: 01/08/24:", bg="orange")

        self.forename.grid(row=1, column=0, padx=5, pady=1, sticky="W")
        self.surname.grid(row=3, column=0, padx=5, pady=1, sticky="W")
        self.mobile.grid(row=5, column=0, padx=5, pady=1, sticky="W", )
        self.date_label.grid(row=7, column=0, padx=5, pady=5)

        self.input_forename = tk.Entry(self.input_order_details, bg="light green")
        self.input_surname = tk.Entry(self.input_order_details, bg="light green")
        self.input_mobile = tk.Entry(self.input_order_details, bg="light green")
        self.date_input = tk.Entry(self.input_order_details, bg="light green")

        self.input_forename.grid(row=2, column=0, padx=5, pady=1, )
        self.input_surname.grid(row=4, column=0, padx=5, pady=1, )
        self.input_mobile.grid(row=6, column=0, padx=5, pady=1, )
        self.date_input.grid(row=8, column=0, padx=5, pady=5)

        self.tutor_picker = tk.OptionMenu(self.input_order_details, self.clicked, *self.tutor_groups, )
        self.tutor_picker.grid(row=1, column=1, padx=5, pady=1, sticky="W")
        self.tutor_picker.config(bg="orange", fg="black")

        self.colour_picker = tk.OptionMenu(self.input_order_details, self.colour_picked, *self.colours, )
        self.colour_picker.grid(row=2, column=1, padx=5, pady=1, sticky="W")
        self.colour_picker.config(bg="orange", fg="black")

        self.size_picker = tk.OptionMenu(self.input_order_details, self.size_picked, *self.sizes, command = self.update_cost)
        self.size_picker.grid(row=3, column=1, padx=5, pady=1, sticky="W")
        self.size_picker.config(bg="orange", fg="black")

        self.quantity = tk.Spinbox(self.input_order_details, from_=1, to=3, command=lambda: self.update_cost())
        self.quantity.grid(row=4, column=1)

        self.submit_button = tk.Button(self.input_order_details, text="Submit Order",
                                       command=lambda: self.submit_order())
        self.submit_button.grid(row=5, column=1, rowspan=2)

        self.info_box = tk.Text(self.input_order_details, height=6, width=40)
        self.info_box.grid(row=7, column=1, columnspan=2, rowspan=6, padx=5, pady=5)

    def open_order_search(self):

        self.tab = 2
        self.intialise_variables()

        self.order_details_search = tk.Frame(self, bg="orange", borderwidth=10, relief="ridge")
        self.order_details_search.grid(row=2, column=0, sticky="n", columnspan=5, padx=15, pady=15)

        self.filter_label = tk.Label(self.order_details_search, text="filters:", bg="orange")
        self.filter_label.grid(row=0, column=0)

        self.info_box = tk.Text(self.order_details_search, height=10, width=50)
        self.info_box.grid(row=0, column=1, rowspan=5)

        self.filter_to_add_label = tk.Label(self.order_details_search, text="filter to add:", bg="orange")
        self.filter_to_add_label.grid(row=0, column=2, padx=3, pady=3)

        self.filter_group_picker = tk.OptionMenu(self.order_details_search, self.filter_picked, *self.possible_filters)
        self.filter_group_picker.grid(row=3, column=2, padx=5, pady=1, )
        self.filter_group_picker.config(bg="orange", fg="black")

        self.item_to_search = tk.Entry(self.order_details_search, bg="light green")
        self.item_to_search.grid(row=2, column=2, padx=3, pady=3)

        self.filter_button = tk.Button(self.order_details_search, text="add filter", command=lambda: self.add_filter())
        self.filter_button.grid(row=4, column=2, padx=3, pady=3)

    def print_receipt(self):

        file = f"{len(self.total_data) + 1}#_Receipt.txt"

        with open(file, "w") as f:
            f.write(self.order_details + "\n")

    def file_reader(self, file):
        # adds all the data in the file as a 2D array

        try:
            self.total_data = []
            with open(file, "r") as f:

                data = f.readlines()
            for personal_data in data:
                self.total_data.append(personal_data.strip().split(" "))
        except:
            self.total_data = ""

    def add_to_file(self, file):

        try:
            with open(file, "a") as f:
                f.write(self.order_details + "\n")
        except:
            with open(file, "w") as f:
                f.write(self.order_details + "\n")

    def intialise_variables(self):

        self.size_picked = tk.StringVar()
        self.size_picked.set("pick a size")

        self.colour_picked = tk.StringVar()
        self.colour_picked.set("pick a colour")

        self.clicked = tk.StringVar()
        self.clicked.set("Select a tutor group")

        self.filter_picked = tk.StringVar()

        self.incomplete_data = True
        self.price = 0
        self.total_filters = []

    def submit_order(self):

        self.file_reader("Master_file.txt")

        conn = sqlite3.connect('hoodies.db')
        cursor = conn.cursor()
        self.data_to_add = self.input_forename.get().lower(), self.input_surname.get().lower(), self.clicked.get().lower(), self.input_mobile.get().lower(), self.date_input.get().lower(), self.colour_picked.get(), self.size_picked.get(), self.price, self.quantity.get()

        cursor.execute("INSERT INTO hoodie (forename, surname, mobile, date, tutor, colour, size, quantity, price ) VALUES (?,?,?,?,?,?,?,?,?)",(self.data_to_add))

        conn.commit()
        conn.close()

        self.order_details = f"{len(self.total_data) + 1, self.input_forename.get().lower(), self.input_surname.get().lower(), self.clicked.get().lower(), self.input_mobile.get().lower(), self.date_input.get().lower(), self.colour_picked.get(), self.size_picked.get(), self.price, self.quantity.get()}"

        self.validate_user_input()

        if self.incomplete_data == True:
            self.info_box.delete(1.0, tk.END)
            self.info_box.insert(tk.END, f"your order has been place, a digital record will be sent to you soon!")

            self.after(1000, lambda: self.clear_screen(1))

    def update_cost(self, pain=True):
        try:

            self.price = int(self.quantity.get()) * self.sizes[self.size_picked.get()]
            self.info_box.delete(1.0, tk.END)
            self.info_box.insert(tk.END, f"hey you got {self.quantity.get()} items, this costs £{self.price}")
        except:

            self.info_box.delete(1.0, tk.END)
            self.info_box.insert(tk.END, f"error with order details")

    def file_searcher(self):

        self.file_reader("Master_file.txt")

        self.records_that_match = []

        for j in range(0, len(self.total_filters)):

            for i in range(0, len(self.total_data)):

                if self.total_data[i][self.total_filters[j][1]].strip(",").strip("(").strip(")").strip("'") == \
                        self.total_filters[j][0]:
                    self.records_that_match.append(self.total_data[i])

        self.info_box.delete(1.0, tk.END)
        self.info_box.insert(tk.END, f"records that match at least one of your filters are,")

        for i in range(0, len(self.records_that_match)):
            self.info_box.insert(tk.END, f"\n{self.records_that_match[i]}")

    def clear_screen(self, tab):

        if tab == 1:
            self.input_order_details.destroy()
            self.open_order_inputs()

        if tab == 2:
            self.order_details_search.destroy()
            self.open_order_search()

    def validate_user_input(self):

        while True:

            if self.input_forename.get() == "":
                break
            if self.input_surname.get() == "":
                break
            if self.input_mobile.get() == "":
                break
            if self.clicked.get() == "Select a tutor group":
                break
            if self.size_picked.get() == "pick a size":
                break
            if self.colour_picked.get() == "pick a colour":
                break

            does_date_match = self.date_pattern.match(self.date_input.get())

            if does_date_match and len(self.date_input.get()) == 8:
                self.add_to_file("Master_file.txt")
                self.print_receipt()
                return

        self.incomplete_data = False
        self.info_box.delete(1.0, tk.END)
        self.info_box.insert(tk.END, f"incomplete order")

    def add_filter(self):

        self.total_filters.append([self.item_to_search.get().lower(), self.possible_filters[self.filter_picked.get()]])

        self.anything()

        self.file_searcher()

    def anything(self):
        self.current_filter_label = tk.Label(self.order_details_search, text=f"filtering for {self.item_to_search.get()}", bg="orange")
        self.current_filter_label.grid(column=0, row=len(self.total_filters))

    def database_searcher(self):

        conn = sqlite3.connect('hoodie.db')
        cursor = conn.cursor()
        cursor.execute(self.query,(self.search_values))
        results = cursor.fetchall()
        for result in results:
            self.info_box.insert(tk.END, f"\n{result}")


if __name__ == "__main__":
    my_win = tk.Tk()
    frame = Hoodies(my_win)
    my_win.mainloop()
