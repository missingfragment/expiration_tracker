from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class PurgePrompt(Toplevel):
    def __init__(self, main_window) -> None:
        super().__init__()

        self.main_window = main_window

        self.title("Purge Prompt")
        self.resizable(False, False)
        self.setup_layout()

    def setup_layout(self) -> None:
        self.mainframe = ttk.Frame(self, padding="5")
        self.mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        self.input_panel = ttk.Frame(self.mainframe, padding="5")
        self.input_panel.grid(column=0, row=1)

        self.button_panel = ttk.Frame(self.mainframe, padding="5")
        self.button_panel.grid(column=0, row=2, sticky=(S, E))

        info_label = ttk.Label(
            self.mainframe, text="Delete all expired records that meet the following criteria:")
        info_label.grid(column=0, row=0)

        self.use_limit = BooleanVar()
        self.age_limit = StringVar()

        input_checkbox = ttk.Checkbutton(
            self.input_panel, variable=self.use_limit, onvalue=True, offvalue=False,
            text="Limit selection to expired records that are older than ").grid(column=0, row=0)

        input_entry = ttk.Entry(
            self.input_panel, textvariable=self.age_limit).grid(column=1, row=0)

        input_unit_label = ttk.Label(
            self.input_panel, text="day(s)").grid(column=2, row=0)

        self.confirm_button = ttk.Button(
            self.button_panel, text="Execute", command=self.execute)
        self.confirm_button.grid(column=0, row=0, sticky=(S, E))

        self.cancel_button = ttk.Button(
            self.button_panel, text="Cancel", command=self.destroy
        )
        self.cancel_button.grid(column=1, row=0, sticky=(N, W))

    def execute(self) -> None:
        use_age_limit: bool = self.use_limit.get()
        age_limit = None
        if use_age_limit:
            try:
                age_limit: int = int(self.age_limit.get())
                if age_limit < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    message="Age limit must be a positive integer.", parent=self,
                    title="Invalid Data")

        self.main_window.purge_records(
            age_limit=age_limit if use_age_limit else None)
        self.destroy()
