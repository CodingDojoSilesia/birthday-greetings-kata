# birthday-greetings-kata

## Goal

As you’re a very friendly person, you would like to send a birthday note to all the friends you have. But you have a lot of friends and a bit lazy, it may take some times to write all the notes by hand. Make your computer do it.

Your program should load data from flat file

    last_name, first_name, date_of_birth, email
    Doe, John, 1982-10-08, john.doe@foobar.com
    Ann, Mary, 1975-09-11, mary.ann@foobar.com

Then it should send messages to a people whose birthday is today.
It is ok if it displays them instead of sending, but...

Design your solution in way that business logic is not coupled with input and output.
As an example if input data delivery will change to a webservice business logic must stay the same, or if it comes from SQLite db.

If you decide to send SMS business logic must stay the same. Or facebook message.

Friends born on February, 29th should have their Birthday greeted on February, 28th.

Think how you can test it.

## Running tests

### I have pipenv

    pipenv install --dev
    pipenv run test

### I don't have pipenv

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    pytest

## Generating your own fake data

Please look into `fake_data.py` and adjust to your hearts content.
