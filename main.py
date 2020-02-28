from typing import Union
from datetime import date
from datetime import datetime

from sources import FileSource
from sources import WebSource
from sources import User

from services import MessageEmailService


class BirtdayService(object):
    def __init__(
        self, source: Union[FileSource, WebSource], message_service: MessageEmailService
    ):
        self.source = source
        self.message_service = message_service

    def send_messages(self, date: date = date.today()) -> None:
        for user in self.source.get_users_by_date(date.month, date.day):
            self.message_service.send_message(user)

message_service = MessageEmailService()


today = datetime.strptime("2012-02-29", "%Y-%m-%d").date()

print("#" * 10, "FILE SOURCE", "#" * 10)
user_file_source = FileSource("input.csv")
file_bday_service = BirtdayService(user_file_source, message_service)
file_bday_service.send_messages(today)

print("#" * 10, "WEB SOURCE", "#" * 10)
user_web_source = WebSource("http://212.47.253.227")
web_bday_service = BirtdayService(user_web_source, message_service)
web_bday_service.send_messages(today)
