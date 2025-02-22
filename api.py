import requests
import json
from dataclasses import dataclass
from typing import Tuple, Dict, Any


@dataclass
class PetFriends:
    base_url: str = "https://petfriends.skillfactory.ru/"

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: Dict[str, str] = None,
        data: Dict[str, Any] = None,
        params: Dict[str, str] = None,
        files: Dict[str, Any] = None,
    ) -> Tuple[int, Any]:
        url = self.base_url + endpoint
        res = requests.request(
            method, url, headers=headers, data=data, params=params, files=files
        )
        try:
            return res.status_code, res.json()
        except json.JSONDecodeError:
            return res.status_code, res.text

    def get_api_key(self, email: str, password: str) -> Tuple[int, Any]:
        headers = {"email": email, "password": password}
        return self._request("GET", "api/key", headers=headers)

    def get_list_of_pets(
        self, auth_key: Dict[str, str], filter: str = ""
    ) -> Tuple[int, Any]:
        headers = {"auth_key": auth_key["key"]}
        params = {"filter": filter}
        return self._request("GET", "api/pets", headers=headers, params=params)

    def add_new_pet(
        self,
        auth_key: Dict[str, str],
        name: str,
        animal_type: str,
        age: str,
        pet_photo: str,
    ) -> Tuple[int, Any]:
        headers = {"auth_key": auth_key["key"]}
        data = {"name": name, "animal_type": animal_type, "age": age}
        with open(pet_photo, "rb") as photo:
            files = {"pet_photo": (pet_photo, photo, "image/jpeg")}
            return self._request(
                "POST", "api/pets", headers=headers, data=data, files=files
            )

    def delete_pet(self, auth_key: Dict[str, str], pet_id: str) -> Tuple[int, Any]:
        headers = {"auth_key": auth_key["key"]}
        return self._request("DELETE", f"api/pets/{pet_id}", headers=headers)

    def update_pet_info(
        self,
        auth_key: Dict[str, str],
        pet_id: str,
        name: str,
        animal_type: str,
        age: int,
    ) -> Tuple[int, Any]:
        headers = {"auth_key": auth_key["key"]}
        data = {"name": name, "age": str(age), "animal_type": animal_type}
        return self._request("PUT", f"api/pets/{pet_id}", headers=headers, data=data)

    def add_new_pet_without_photo(
        self, auth_key: Dict[str, str], name: str, animal_type: str, age: str
    ) -> Tuple[int, Any]:
        headers = {"auth_key": auth_key["key"]}
        data = {"name": name, "animal_type": animal_type, "age": age}
        return self._request(
            "POST", "api/create_pet_simple", headers=headers, data=data
        )

    def add_pet_photo(
        self, auth_key: Dict[str, str], pet_id: str, pet_photo: str
    ) -> Tuple[int, Any]:
        headers = {"auth_key": auth_key["key"]}
        with open(pet_photo, "rb") as photo:
            files = {"pet_photo": (pet_photo, photo, "image/jpeg")}
            return self._request(
                "POST", f"api/pets/set_photo/{pet_id}", headers=headers, files=files
            )
