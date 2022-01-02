from tkinter import *
from src.expiration_entry import ExpirationEntry
from src.gui.expiration_tracker import ExpirationTracker
from src.file_manager import CsvFileStatus, FileManager
from src.record_set import RecordSet
from datetime import date, timedelta
from pathlib import Path
import sys


def main():
    csv_file = Path('data.csv')
    fm = FileManager(csv_file)

    if fm.csv_initial_state == CsvFileStatus.OPENED:
        records = RecordSet(fm.load_records())
    else:
        records = RecordSet()

    print("Expiration Tracker\n------")
    while True:
        prompt = "\n1: Create record\n2: List records\n3: Delete records\n4: Search Records\nType \"exit\" to finish program."
        try:
            command = input(prompt)
            if command == "1":
                new_record = create_record()
                if new_record:
                    records.add(new_record)
                    fm.update_records(records.dict)
                    input("Successfully saved record.")

            elif command == "2":
                records.print()
                input("...")
            elif command == "3":
                delete_record(fm, records)
                input("...")
            elif command == "4":
                search_records(fm, records)
                input("...")
            elif command == "exit" or command == "":
                break

        except EOFError:
            print("Operation cancelled.  Ending program.")
            break


def delete_record(fm: FileManager, records: RecordSet) -> None:

    while True:
        matches = search_records(
            fm, records, prompt="Enter the name of the record you wish to delete."
        )

        if not matches:
            break

        while True:
            record = None
            which = input(
                "Enter the number of the entry you wish to delete, " +
                "or leave blank to start over."
            )

            if not which or which == "":
                break

            try:
                which = int(which)
            except ValueError:
                print("Please enter a number.")
                continue

            index = which-1
            if index < 0 or index >= len(matches):
                print("Please enter one of the displayed numbers.")
                continue

            record = matches[index]
            break
        if not record:
            break

        key = record.get_id()
        if records.delete(key):
            print("Deleted successfully.")
            fm.update_records(records.dict)
        else:
            print("Something went wrong, please try again.")
        break


def search_records(fm, records, prompt="Enter the name of the record you're looking for.") -> list:
    while True:
        name = input(
            f"{prompt}  Enter \".\" to stop.")

        if name == "." or not name or name == "":
            break

        matches = [
            record for record in records.dict.values() if record.name == name
        ]

        if not matches:
            print(
                f"No record with the name \"{name!r}\" was found."
            )
            continue

        print("Found the following records with matching names:")
        i = 1
        for match in matches:
            print(f"{i!s}) {match!s}")
            i += 1
        return matches
    return None


def create_record() -> ExpirationEntry:
    try:
        name = input("Enter a name for the entry.")
        while True:
            start_date_string = input(
                'Enter the starting date.  (Type "today" to use the current date.)')
            if start_date_string.lower() == "today":
                start_date = date.today()
            else:
                try:
                    start_date = date.fromisoformat(start_date_string)
                except ValueError:
                    print('Invalid date.  Please enter in ISO format.  (YYYY-MM-DD)')
                    continue
            break
        while True:
            duration_string = input(
                'Enter the number of days after which the entry will expire.')
            try:
                duration_int = int(duration_string)
            except ValueError:
                print("Please enter a number.")
                continue
            if duration_int < 0:
                print('Invalid duraiton.  Please enter a non-negative integer value.')
                continue
            duration = timedelta(days=duration_int)
            break

        new_entry = ExpirationEntry(name, start_date, duration)

        print("New entry: {}".format(new_entry))

        confirm = ""
        while confirm.lower() != "y" and confirm.lower() != "n":
            confirm = input("Save entry?  Type Y to save or N to discard.")

        confirmation = confirm.lower() == "y"

        if confirmation:
            return new_entry
        else:
            input("Discarding record.")
            return None

    except EOFError:
        return


if len(sys.argv) > 1 and sys.argv[1] == "cl":
    main()
else:
    root = Tk()
    root.option_add('*tearOff', FALSE)
    gui = ExpirationTracker(root)
    root.columnconfigure(0, weight=1, minsize=600)
    root.rowconfigure(1, weight=1, minsize=300)
    root.minsize(width=600, height=400)
    root.mainloop()
