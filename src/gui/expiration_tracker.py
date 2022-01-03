from tkinter import *
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from src.expiration_entry import ExpirationEntry

from src.file_manager import FileManager, CsvFileStatus
from src.record_set import RecordSet
from src.gui.new_record_prompt import NewRecordPrompt
from src.gui.purge_prompt import PurgePrompt
from src.gui.settings_window import SettingsWindow

from datetime import date, timedelta

from functools import partial


class ExpirationTracker:
    def __init__(self, root: Toplevel) -> None:
        root.title("Expiration Tracker")
        root.geometry("600x500")

        self.root = root

        self.csv_file = Path("data.csv")
        self.file_manager = FileManager(self.csv_file)

        if self.file_manager.csv_initial_state == CsvFileStatus.OPENED:
            records = RecordSet(self.file_manager.load_records())
        else:
            records = RecordSet()

        self.records = records

        self.entry_rows = []

        self.mainframe = ttk.Frame(root, padding="10")
        self.mainframe.grid(column=0, row=1, sticky=(N, W, E, S))

        self.button_panel = ttk.Frame(root, padding="10")
        self.button_panel.grid(column=0, row=0, sticky=(N, S, E, W))

        self.init_config()
        self.init_layout()
        self.init_menubar(root)
        self.update_layout()

    def init_config(self) -> None:
        self.config = {
            "auto_save": False
        }

    def init_menubar(self, root) -> None:
        menubar = Menu(root)
        root['menu'] = menubar
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label="File")
        menubar.add_cascade(menu=menu_edit, label="Edit")

        menu_file.add_command(
            label="New Record Set",
            command=self.new_record_set
        )
        menu_file.add_command(
            label="Import Record Set...",
            command=self.import_record_set
        )
        menu_file.add_command(
            label="Export Record Set...",
            command=self.export_record_set
        )

        menu_file.add_separator()

        menu_file.add_command(
            label="Settings",
            command=(lambda: SettingsWindow(self))

        )
        menu_file.add_separator()

        menu_file.add_command(
            label="Exit",
            command=(lambda: self.root.destroy())
        )

        menu_edit.add_command(
            label="Add Record...",
            command=self.add_button.invoke
        )

        menu_edit.add_command(
            label="Purge Records...",
            command=self.purge_button.invoke
        )

    def new_record_set(self) -> None:
        file_types = [("CSV Files", ".csv")]

        filename = filedialog.asksaveasfilename(
            filetypes=file_types, defaultextension=".csv")

        if filename:
            self.records = RecordSet()
            self.file_manager.csv_file = Path(filename)
            self.update()

    def import_record_set(self) -> None:
        file_types = [
            ("CSV Files", ".csv"),
            ("All Files", ".*")
        ]

        filename = filedialog.askopenfilename(filetypes=file_types)

        if filename:
            filename = Path(filename).resolve()
            result = self.file_manager.import_records(filename)

            if result:
                self.records = RecordSet(self.file_manager.load_records())
                self.update()

    def export_record_set(self) -> None:
        file_types = [("CSV Files", ".csv")]

        filename = filedialog.asksaveasfilename(
            filetypes=file_types, defaultextension=".csv")

        if filename:
            filename = Path(filename).resolve()
            result = self.file_manager.export_records(
                self.records.dict, filename)

            print("result: {}".format(result))

    def init_layout(self) -> None:
        # header row
        header_name = ttk.Label(
            self.mainframe, text="Name").grid(column=1, row=1)
        header_start = ttk.Label(
            self.mainframe, text="Start Date").grid(column=2, row=1)
        header_duration = ttk.Label(
            self.mainframe, text="Duration").grid(column=3, row=1)
        header_expiration = ttk.Label(
            self.mainframe, text="Expiration Date").grid(column=4, row=1)
        header_remaining = ttk.Label(
            self.mainframe, text="Remaining Day(s)").grid(column=5, row=1)

        self.add_button = ttk.Button(
            self.button_panel, text="Add", command=self.new_record)
        self.add_button.grid(column=0, row=0, sticky=(N, W))

        self.purge_button = ttk.Button(
            self.button_panel, text="Purge", command=self.purge_prompt
        )
        self.purge_button.grid(column=1, row=0, sticky=(N, W))

    def update_layout(self) -> None:
        for row in self.entry_rows:
            for entry in row:
                entry.destroy()

        self.entry_rows = []
        row = 2
        for record in self.records.dict.values():
            new_row = []
            name_label = ttk.Label(self.mainframe)

            name_label["text"] = record.name
            name_label.grid(column=1, row=row, sticky=(N, S, E, W))

            new_row.append(name_label)

            start_label = ttk.Label(self.mainframe)

            start_label["text"] = record.start_date
            start_label.grid(column=2, row=row, sticky=(N, S, W, E))

            new_row.append(start_label)

            duration_label = ttk.Label(self.mainframe)
            duration_label["text"] = str(record.duration.days)
            duration_label.grid(column=3, row=row, sticky=(N, S, E, W))

            new_row.append(duration_label)

            expiration_label = ttk.Label(self.mainframe)
            expiration_label["text"] = str(record.expiration_date)
            expiration_label.grid(column=4, row=row, sticky=(N, S, E, W))

            new_row.append(expiration_label)

            remaining_days = record.get_remaining_days(date.today()).days

            remaining_label = ttk.Label(self.mainframe)
            if remaining_days < 0:
                remaining_label["text"] = "EXPIRED {} days ago".format(
                    abs(remaining_days))
            else:
                remaining_label["text"] = str(remaining_days)
            remaining_label.grid(column=5, row=row, sticky=(N, S, E, W))

            new_row.append(remaining_label)

            delete_button = ttk.Button(
                self.mainframe, text="Delete",
                command=partial(self.delete_record, record.get_id())
            )
            delete_button.grid(column=6, row=row, sticky=W)

            new_row.append(delete_button)

            self.entry_rows.append(new_row)
            row += 1

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def new_record(self) -> None:
        prompt = NewRecordPrompt(self)

    def add_record(self, new_record: ExpirationEntry) -> None:
        self.records.add(new_record)
        self.update()

    def purge_prompt(self) -> None:
        prompt = PurgePrompt(self)

    def delete_record(self, key: str) -> None:
        confirm = messagebox.askyesno(message="Delete record?")

        if confirm == False:
            return

        self.records.delete(key)
        self.update()

    def update(self) -> None:
        self.file_manager.update_records(self.records.dict)
        self.update_layout()

    def purge_records(self, age_limit: int = None):
        matches = []

        if age_limit:
            date_cutoff = date.today() - timedelta(days=age_limit)
            print(date_cutoff)
            matches = [
                record for record in self.records.dict.values()
                if record.is_expired() and record.expiration_date <= date_cutoff
            ]
        else:
            matches = [
                record for record
                in self.records.dict.values()
                if record.is_expired()
            ]

        if not matches or len(matches) == 0:
            messagebox.showinfo(
                message="No records matching the criteria were found.", title="Operation Failed")
            return
        self.mass_delete(matches)

    def mass_delete(self, records: list[ExpirationEntry]) -> None:
        warning_message = "This operation will delete {} record(s).  Is this ok?".format(
            len(records))

        confirm = messagebox.askokcancel(
            message=warning_message, title="Delete Confirmation")

        if not confirm:
            return

        for record in records:
            self.records.delete(record.get_id())
        self.update()
