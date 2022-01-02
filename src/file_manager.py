from pathlib import Path
from .expiration_entry import ExpirationEntry
import csv
from enum import Enum


class CsvFileStatus(Enum):
    CREATED = 1
    OPENED = 2


class FileManager:
    def __init__(self, csv_file: Path) -> None:
        self.csv_file = csv_file
        assert not csv_file.is_dir()

        if not csv_file.exists():
            csv_file.touch()
            self.csv_initial_state = CsvFileStatus.CREATED
        else:
            self.csv_initial_state = CsvFileStatus.OPENED

    def update_records(self, data: dict[str, ExpirationEntry]) -> None:
        self.write_data(data, self.csv_file)

    def load_records(self) -> dict:
        records = {}
        with self.csv_file.open(mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entry = ExpirationEntry.from_dict(row)
                records[entry.get_id()] = entry

        return records

    def export_records(self, data: dict[str, ExpirationEntry],
                       save_path: Path) -> bool:
        self.write_data(data, save_path)

        return True

    def import_records(self, csv_file: Path) -> bool:
        if not csv_file.exists() or not csv_file.is_file():
            return False
        self.csv_file = csv_file

        return True

    def write_data(self, data: dict[str, ExpirationEntry], path: Path) -> None:
        if not path.exists():
            path.touch()

        with path.open(mode='w') as f:

            writer = csv.DictWriter(f, fieldnames=ExpirationEntry.fieldnames)

            writer.writeheader()

            for entry in data.values():
                writer.writerow(entry.get_data())
