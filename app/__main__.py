import abc
import csv
import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Dict, List, Optional, Generator

import dateutil
import dateutil.parser


@dataclass
class Person:
    address: str
    data: Dict[str, Union[str, datetime.datetime]]


class BaseResource(abc.ABC):

    @abc.abstractmethod
    def connect(self):
        ...

    @abc.abstractmethod
    def parse(self):
        ...


class CSVResource(BaseResource):
    def __init__(self, path):
        self._path = path
        self._reader: Optional[List[Dict[str, Union[str, datetime]]]] = None

    def connect(self) -> None:
        with open(self._path, mode='r') as csv_input:
            self._reader = list(csv.DictReader(csv_input))

    def parse(self) -> Generator:
        assert self._reader
        for person in self._reader:
            yield Person(address=person[' email'], data=person)


class Handler:
    def __init__(self, resource: BaseResource):
        self._resource = resource

    def _select_birthday_person(self, person_data):
        person_birthday = dateutil.parser.parse(person_data[" date_of_birth"])

        if int(person_birthday.month) == datetime.datetime.today().month == 2 \
                and person_birthday.day == '29' and datetime.datetime.today().day == 28:
            return True

        elif person_birthday.day == datetime.date.today().day \
                and int(person_birthday.month) == datetime.datetime.today().month:
            return True

        return False

    def build_birthdays_people(self):
        persons = self._resource.parse()
        persons_with_today_birthday = filter(lambda person: self._select_birthday_person(person.data), persons)
        return persons_with_today_birthday


class Sender:
    def __init__(self, handler, service, message='Happy Birthday from Coding Dojo 2020!'):
        self.handler = handler
        self.service = service
        self.message = message

    def prepare_final_messages(self):
        people = self.handler.build_birthdays_people()
        final_data = {}
        for person in people:
            final_data[person.address] = self.generate_message_for_person(person)

        return final_data

    def generate_message_for_person(self, person):
        fine_greeting = f"Dear {person.data[' first_name']}! {self.message}"
        return fine_greeting

    def send(self):
        for address, msg in self.prepare_final_messages().items():
            self.service("Where: {:40} | Message: {:>25}".format(address, msg))


class ConsoleService():
    def make_method(self):
        return print


if __name__ == '__main__':
    current_path = Path(__file__).resolve()
    path = current_path.parent.parent / 'input.csv'

    resource = CSVResource(path)
    resource.connect()

    handler = Handler(resource)

    service = ConsoleService()

    sender = Sender(handler, service.make_method())
    sender.send()
