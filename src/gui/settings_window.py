from tkinter import *
from tkinter import ttk

import sys
from tkinter import messagebox


class SettingsWindow(Toplevel):
    def __init__(self, parent=None):
        super().__init__()

        if parent:
            self.parent = parent

        self.title("Settings")
        self.geometry("600x500")
        self.minsize(width=400, height=500)

        self.settings = {}
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.setup_layout()

    def setup_layout(self):
        self.canvas = Canvas(self, borderwidth=0)
        self.mainframe = ttk.Frame(self.canvas, padding="5")

        self.canvas.grid(column=1, row=0, sticky=(N, S, W, E))

        self.scrollbar = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(column=2, row=0, sticky=NSEW)

        row = 0
        self.settings['auto_save'] = BooleanVar()
        self.auto_save_checkbox = ttk.Checkbutton(
            self.mainframe, text="Auto-save", variable=self.settings['auto_save']
        ).grid(column=0, row=row, sticky=(N, E, W))
        row += 1

        categories = ["General", "Other"]
        categories_var = StringVar(value=categories)

        self.listbox = Listbox(
            self, listvariable=categories_var, borderwidth=10, relief="flat"
        ).grid(column=0, row=0, sticky=NSEW)

        self.canvas.create_window(
            (0, 0), window=self.mainframe, anchor=NW, tags="self.mainframe")
        self.mainframe.bind("<Configure>", self.on_frame_configure)

        self.button_contianer = ttk.Frame(self, padding="5")

        self.apply_button = ttk.Button(
            self.button_contianer, text="Apply", command=self.apply_settings
        ).grid(column=0, row=0, sticky=NSEW)
        self.cancel_button = ttk.Button(
            self.button_contianer, text="Cancel", command=self.cancel
        ).grid(column=1, row=0, sticky=NSEW)

        self.button_contianer.grid(column=1, row=1, sticky=E)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def apply_settings(self):
        self.parent.config['auto_save'] = self.settings['auto_save'].get()
        messagebox.showinfo(self, "Settings applied.")

    def cancel(self):
        confirm = messagebox.askokcancel(
            self,
            title="Confirmation",
            message="Closing this window and discarding changes.  Is this ok?"
        )
