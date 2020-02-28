import csv
from typing import Iterable
from dataclasses import dataclass
from datetime import date, datetime

import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup


def str_to_date_tuple(date: str) -> date:
    d = datetime.strptime(date, "%Y-%m-%d")
    return (d.month, d.day)


@dataclass
class User:
    last_name: str
    first_name: str
    date_of_birth: date
    email: str


class FileSource(object):
    def __init__(self, fname: str):
        self.fname = fname

    def get_users_by_date(self, month: int, day: int) -> Iterable[User]:
        with open(self.fname, "r") as fp:
            reader = csv.reader(fp)
            next(reader)  # header drop
            for line in reader:
                last_name, first_name, birthdate, email = line
                bday_month, bday_day = str_to_date_tuple(birthdate.strip())
                is_february_28 = month == 2 and day == 28
                if bday_month == month and bday_day == day:
                    yield User(last_name, first_name, birthdate, email)
                # people born at 29th of February should be taken into consideration
                # at 28th of February
                if is_february_28 and bday_day == 29:
                    yield User(last_name, first_name, birthdate, email)


class WebServerDown(Exception):
    pass


class WebSource(object):
    def __init__(self, url: str):
        self.url = url
        try:
            self.content = requests.get(url).content
        except ConnectionError:
            raise WebServerDown(
                "Sorry, couldn't connect to server. Check if it's up and working."
            )

    def get_users_by_date(self, month: int, day: int) -> Iterable[User]:
        bs = BeautifulSoup(self.content, "html.parser")
        table = bs.find("table")
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            last_name, first_name, birthdate, email = (ele.text.strip() for ele in cols)
            bday_month, bday_day = str_to_date_tuple(birthdate)
            is_february_28 = month == 2 and day == 28
            if bday_month == month and bday_day == day:
                yield User(last_name, first_name, birthdate, email)

            # people born at 29th of February should be taken into consideration
            # at 28th of February
            if is_february_28 and bday_day == 29:
                yield User(last_name, first_name, birthdate, email)

