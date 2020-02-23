import freezegun

from marilyn import monroe


@freezegun("2020-05-22")
def test_one_case():
    messages = monroe().send_messages()

    assert "Michał Klich" in messages
