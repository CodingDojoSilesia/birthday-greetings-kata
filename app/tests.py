from pathlib import Path

from freezegun import freeze_time  # type: ignore
from pytest import fixture  # type: ignore

from .__main__ import CSVResource, Handler, BaseResource, Person


@fixture
def birthday_normal():
    person = Person(
        address="uwright@hotmail.com",
        data={
            " last_name": "Turner",
            " first_name": "Charles",
            " date_of_birth": "1997-09-14",
            " email": "uwright@hotmail.com",
        }
    )

    return [person]


@fixture
def birthday_february_29():
    person = Person(
        address="uwright@hotmail.com",
        data={
            " last_name": "Turner",
            " first_name": "Charles",
            " date_of_birth": "2020-02-29",
            " email": "uwright@hotmail.com",
        }
    )
    return [person]


class MockResource(BaseResource):
    def __init__(self, fixture):
        self.fixture = fixture

    def parse(self):
        return self.fixture

    def connect(self):
        ...


def test_csv_connector_is_connected():
    current_path = Path(__file__).resolve()
    path = current_path.parent.parent / 'input.csv'
    csv_resource = CSVResource(path)
    csv_resource.connect()

    assert csv_resource._reader is not None


def test_csv_connector():
    current_path = Path(__file__).resolve()
    path = current_path.parent.parent / 'input.csv'
    csv_resource = CSVResource(path)
    csv_resource.connect()

    assert list(csv_resource.parse())[0].address.strip() == 'uwright@hotmail.com'


@freeze_time("2020-09-14")
def test_select_birthday_person(birthday_normal):
    handler = Handler(resource=MockResource(birthday_normal))

    assert len(list(handler.build_birthdays_people())) == 1


@freeze_time("2020-02-29")
def test_select_birthda_person_02_29(birthday_february_29):
    handler = Handler(resource=MockResource(birthday_february_29))
    assert len(list(handler.build_birthdays_people())) == 1
