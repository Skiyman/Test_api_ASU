import pytest

from tests.conftest import pf, generate_string, russian_chars, chinese_chars, special_chars


@pytest.mark.parametrize("password", ["123456"], ids=["invalid pass"])
@pytest.mark.parametrize("email", ["ffff@hhhh.gg"], ids=["invalid email"])
def test_get_api_key_for_valid_user_negative(email, password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert "key" not in result


@pytest.fixture(scope="module")
def pet_id(auth_key):
    status, result = pf.add_new_pet_without_photo({"key": auth_key}, "Plux", "cat", "2")
    assert status == 200
    return result["id"]


@pytest.mark.parametrize("name, animal_type, age", [
    ("Marsel", "cat", "7"),
    ("Buddy", "dog", "3"),
    ("Tweety", "bird", "1"),
    ("Goldie", "fish", "2"),
    ("Speedy", "turtle", "5")
], ids=["cat", "dog", "bird", "fish", "turtle"])
def test_add_new_pet_with_valid_data(auth_key, name, animal_type, age):
    status, result = pf.add_new_pet_without_photo({"key": auth_key}, name, animal_type, age)
    assert status == 200
    assert result["name"] == name
    pf.delete_pet({"key": auth_key}, result["id"])


def test_add_new_pet_with_invalid_key(
    auth_key,
    name="Marsel",
    animal_type="cat",
    age="3",
    pet_photo="tests/images/astolfo-fate-1-1.jpg",
):
    auth_key = {"key": "44f22dc2e04c75cb7b7bdb05419a5fb3f2286de4fa213a75c2c5e50"}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    assert "Please provide &#x27;auth_key&#x27;" in result


@pytest.mark.xfail
def test_add_new_pet_with_invalid_age(
    auth_key, name="Marsel", animal_type="cat", age="r", pet_photo="tests/images/astolfo-fate-1-1.jpg"
):
    """Их шикарное api жрет что угодно в возраст, потому не работает"""
    auth_key = {"key": auth_key}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert "age should be numeric" in result


def test_delete_existing_pet(auth_key, pet_id):
    status, _ = pf.delete_pet({"key": auth_key}, pet_id)
    assert status == 200


def test_successful_update_self_pet_info(
    auth_key, name="Plu", animal_type="cat", age=1
):
    auth_key = {"key": auth_key}
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) > 0:
        status_code, res = pf.update_pet_info(
            auth_key, my_pets["pets"][0]["id"], name, animal_type, age
        )

        assert status_code == 200
        assert res["name"] == name
    else:
        raise Exception("There is no my pets")


def test_add_photo_for_pet(auth_key, pet_photo="tests/images/astolfo-fate-1-1.jpg"):
    auth_key = {"key": auth_key}
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet_without_photo(auth_key, "Plux", "cat", "2")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    _pet_id = my_pets["pets"][0]["id"]
    status, result = pf.add_pet_photo(auth_key, _pet_id, pet_photo)
    assert status == 200
    assert result["pet_photo"] != ""


@pytest.mark.parametrize(
    "filter", ["", "my_pets"], ids=["empty string", "only my pets"]
)
def test_get_all_pets_with_valid_key(auth_key, filter):
    auth_key = {"key": auth_key}

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0


@pytest.mark.parametrize(
    "filter",
    [
        generate_string(255),
        generate_string(1001),
        russian_chars(),
        russian_chars().upper(),
        chinese_chars(),
        special_chars(),
        123,
    ],
    ids=[
        "255 symbols",
        "more than 1000 symbols",
        "russian",
        "RUSSIAN",
        "chinese",
        "specials",
        "digit",
    ],
)
def test_get_all_pets_with_negative_filter(auth_key, filter):
    auth_key = {"key": auth_key}

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
