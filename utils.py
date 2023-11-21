from exceptions import (
    NegativeTitlesError, ImpossibleTitlesError, InvalidYearCupError
)
from datetime import datetime


def data_processing(national_team: dict):
    first_cup = national_team["first_cup"]
    first_cup_formatted = datetime.strptime(first_cup, "%Y-%m-%d")
    first_cup_year = first_cup_formatted.year
    number_titles = national_team["titles"]
    current_year = datetime.now().year

    if number_titles < 0:
        raise NegativeTitlesError("titles cannot be negative")

    if first_cup_year < 1930:
        raise InvalidYearCupError("there was no world cup this year")

    elif first_cup_year >= 1930:
        year_difference = first_cup_year - 1930
        if year_difference % 4 != 0:
            raise InvalidYearCupError("there was no world cup this year")

    if ((current_year - first_cup_year) // 4) < number_titles:
        raise ImpossibleTitlesError(
            "impossible to have more titles than disputed cups"
        )


data = {
    "name": "França",
    "titles": -3,
    "top_scorer": "Zidane",
    "fifa_code": "FRA",
    "first_cup": "2000-10-18",
}

data1 = {
    "name": "França",
    "titles": 3,
    "top_scorer": "Zidane",
    "fifa_code": "FRA",
    "first_cup": "1911-10-18",
}

data2 = {
    "name": "França",
    "titles": 9,
    "top_scorer": "Zidane",
    "fifa_code": "FRA",
    "first_cup": "2002-10-18",
}


data_processing(data2)
