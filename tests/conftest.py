import pytest

from api import PetFriends
from settings import valid_email, valid_password

def generate_string(num):
    return "x" * num


def russian_chars():
    return "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def chinese_chars():
    return "的一是不了人我在有他这为之大来以个中上们"


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


pf = PetFriends()

@pytest.fixture(scope="module")
def auth_key():
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert "key" in result
    return result["key"]
