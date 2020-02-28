from sources import User

import random

emotes = ["( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "( ͡ʘ ͜ʖ ͡ʘ)", "(▀̿Ĺ̯▀̿ ̿)", "( ͡° ͜ʖ ͡°)╭∩╮", "(° ͜ʖ °)", "( ಠ ͜ʖಠ)", "( ͡~ ͜ʖ ͡°)", "༼  ͡° ͜ʖ ͡° ༽"]

class MessageEmailService(object):
    def send_message(self, user: User) -> None:
        emote = random.choice(emotes)
        print(f"Get gnomed {emote} *{user.first_name} {user.last_name}! *")
