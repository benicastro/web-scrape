import requests
from rich import print
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class CharFilter:
    name: Optional[str] = None
    status: Optional[str] = None
    gender: Optional[str] = None
    species: Optional[str] = None
    page: Optional[int] = None


base_url = "https://rickandmortyapi.com/api/character/"


def get_character_one_param(char_id):
    resp = requests.get(base_url + str(char_id))
    print(resp.json())


def search_character(search):
    resp = requests.get(base_url, params=search)
    print(resp.json())


def main():
    search = CharFilter(
        name="rick",
        status="dead",
    )
    search_character(search=asdict(search))


if __name__ == "__main__":
    main()
