from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date, timedelta
from src.expiration_entry import ExpirationEntry


class NewRecordPrompt(Toplevel):
    def __init__(self, main_window) -> None:
        super().__init__()

        self.main_window = main_window

        self.title("New Record...")

        self.setup_layout()
        self.resizable(False, False)

    def setup_layout(self) -> None:
        today = date.today()
        self.name_value = StringVar()
        self.month_value = StringVar()
        self.day_value = StringVar()
        self.year_value = StringVar()
        self.duration_value = StringVar()

        days = list(range(1, 32))
        months = list(range(1, 13))
        years = list(range(1990, 2100))

        self.mainframe = ttk.Frame(self, padding="5")
        self.mainframe.grid(column=0, row=0)

        self.name_panel = ttk.Frame(self.mainframe, padding="3")
        self.name_panel.grid(column=1, row=0, sticky=W)

        self.name_label = ttk.Label(self.mainframe, text="Name: ")
        self.name_label.grid(column=0, row=0)

        self.name_entry = ttk.Entry(
            self.name_panel, textvariable=self.name_value)
        self.name_entry.grid(column=0, row=0)

        self.date_panel = ttk.Frame(self.mainframe, padding="3")
        self.date_panel.grid(column=1, row=1)

        self.date_label = ttk.Label(self.mainframe, text="Start Date: ")
        self.date_label.grid(column=0, row=1)

        self.month_entry = ttk.Combobox(
            self.date_panel, textvariable=self.month_value)
        self.month_entry['values'] = months
        self.month_entry.grid(column=1, row=0)
        self.month_entry.state(["readonly"])
        self.month_entry.set(today.month)

        self.day_entry = ttk.Combobox(
            self.date_panel, textvariable=self.day_value, values=days)
        self.day_entry.grid(column=2, row=0)
        self.day_entry.state(["readonly"])
        self.day_entry.set(today.day)

        self.year_entry = ttk.Combobox(
            self.date_panel, textvariable=self.year_value, values=years)
        self.year_entry.grid(column=3, row=0)
        self.year_entry.set(today.year)

        self.duration_panel = ttk.Frame(self.mainframe, padding="3")
        self.duration_panel.grid(column=1, row=2, sticky=W)

        self.duration_label = ttk.Label(self.mainframe, text="Duration: ")
        self.duration_label.grid(column=0, row=2)

        self.duration_entry = ttk.Entry(
            self.duration_panel, textvariable=self.duration_value)
        self.duration_entry.grid(column=0, row=0, sticky=W)

        self.duration_units_label = ttk.Label(
            self.duration_panel, text="day(s)")
        self.duration_units_label.grid(column=1, row=0, sticky=W)

        button_panel = ttk.Frame(self.mainframe, padding="3")
        button_panel.grid(column=1, row=3, sticky=E)

        self.add_button = ttk.Button(
            button_panel, text="Add", command=self.complete)
        self.add_button.grid(column=0, row=0, sticky=(N, W))
        self.add_button['state'] = ACTIVE

        self.cancel_button = ttk.Button(
            button_panel, text="Cancel", command=self.destroy)
        self.cancel_button.grid(column=1, row=0, sticky=(N, W))

    def close(self) -> None:
        self.destroy()

    def complete(self) -> None:
        name = self.name_value.get()
        try:
            year = int(self.year_value.get())
            month = int(self.month_value.get())
            day = int(self.day_value.get())
            start_date = date(year, month, day)
        except ValueError:
            messagebox.showwarning(
                message="Invalid date.  Please check your input.",
                parent=self, title="Invalid Data")
            return

        try:
            duration_int = int(self.duration_value.get())
            if duration_int < 0:
                raise ValueError

            duration = timedelta(days=duration_int)
        except ValueError:
            messagebox.showwarning(
                message="Invalid duration.  Please make sure that it's a positive integer.",
                parent=self, title="Invalid Data")
            return

        new_record = ExpirationEntry(name, start_date, duration)
        self.main_window.add_record(new_record)
        self.close()
