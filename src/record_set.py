from .expiration_entry import ExpirationEntry


class RecordSet:
    def __init__(self, initial_values: dict[str, ExpirationEntry] = {}) -> None:
        self.dict: dict[str, ExpirationEntry] = initial_values

    def add(self, new_record: ExpirationEntry) -> None:
        self.dict[new_record.get_id()] = new_record

    def delete(self, key: str) -> bool:
        if not key in self.dict.keys():
            print("Record not found.  Unable to delete.")
            return False
        self.dict.pop(key)
        return True

    def get(self, key: str) -> ExpirationEntry:
        return self.dict.get(key)

    def clear(self) -> None:
        self.dict.clear()

    def print(self) -> None:
        if len(self.dict.values()) == 0:
            print("No entries found.")
            return
        for entry in self.dict.values():
            print(entry)
