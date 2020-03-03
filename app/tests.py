import pytest
from freezegun import freeze_time
from pytest import fixture

from .main import CSVResource, Handler, BaseResource


@fixture
def birthday_normal():
    person_data = dict(
        last_name = "Turner",
        first_name = "Charles",
        date_of_birth = "1997-09-14",
        email = "uwright@hotmail.com"
    )
    return [person_data]

@fixture
def birthday_february_29():
    person_data = dict(
        last_name = "Turner",
        first_name = "Charles",
        date_of_birth = "2020-02-29",
        email = "uwright@hotmail.com"
    )
    return [person_data]

class MockResource(BaseResource):
    def __init__(self, fixture):
        self.fixture = fixture

    def parse(self):
        return self.fixture
    def connect(self):
        ...

def test_csv_connector_is_connected():
    csv_resource = CSVResource('../input.csv')

    csv_resource.connect()

    assert csv_resource._reader is not None


def test_csv_connector():
    csv_resource = CSVResource('../input.csv')
    csv_resource.connect()

    assert list(csv_resource.parse())[0]['last_name'] == 'Turner'

@pytest.mark.xfail
@freeze_time("2020-09-14")
def test_select_birthday_person(birthday_normal):
    handler = Handler(resource = MockResource(birthday_normal))

    assert len(list(handler.build_birthdays_people())) == 1

@pytest.mark.xfail
@freeze_time("2020-02-29")
def test_select_birthda_person_02_29(birthday_february_29):
    handler = Handler(resource=MockResource(birthday_february_29))
    assert len(list(handler.build_birthdays_people())) == 1