from datetime import date, timedelta


class ExpirationEntry:
    fieldnames = ['name', 'start_date', 'duration']

    def __init__(self, name: str, start_date: date, duration: timedelta) -> None:
        self.name = name
        self.start_date = start_date
        self.duration = duration

        self.expiration_date = self.start_date + self.duration

    def get_remaining_days(self, reference_date: date) -> timedelta:
        return self.expiration_date - reference_date

    def get_id(self) -> str:
        return "{}_{}".format(self.start_date, self.name)

    def get_data(self) -> dict:
        data = {}
        data['name'] = self.name
        data['start_date'] = self.start_date
        # Remove the time information when exporting, as it is irrelevant
        data['duration'] = str(self.duration).split()[0]
        return data

    def is_expired(self) -> bool:
        return date.today() > self.expiration_date

    @classmethod
    def from_dict(cls, data: dict):
        time_delta_string: str = data['duration']
        try:
            days = int(time_delta_string.split()[0])
        except ValueError:
            print("Creating ExpirationEntry with invalid duration")
        time_delta = timedelta(days=days)
        return cls(data['name'], date.fromisoformat(data['start_date']), time_delta)

    def __str__(self):
        if self.is_expired():
            return "{}\nTHIS ENTRY EXPIRED ON {}, which was {} ago.\n".format(
                self.name, self.expiration_date, str(abs(self.get_remaining_days(
                    date.today())).days)
            )
        return "{}\nStart date: {}\nDuration: {}\nExpiration Date: {} ({} remaining)\n".format(
            self.name, self.start_date, str(self.duration).split(",")[0],
            self.expiration_date, str(
                self.get_remaining_days(date.today()).days)
        )

    def __repr__(self):
        return str(self)
