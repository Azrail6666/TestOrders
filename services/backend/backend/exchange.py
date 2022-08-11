import json
import logging

import requests

from xml.etree import ElementTree as ET
from backend.dbModels.order import Order
from backend.dbModels.order import db
from pathlib import Path

with open(Path(Path.cwd(), "config", "course.json"), 'r') as file:
    course = json.load(file)['course']



def dollars_to_rubles(dollars_sum: float) -> float:
    """
    The function of getting the amount in rubles relative to the given amount in dollars
    :param dollars_sum: Amount in dollars
    :return: Amount in dollars
    """
    return round(float(dollars_sum * course), 2)


def get_new_course() -> float:
    """
    The function of obtaining the current exchange rate of the Central Bank of the Russian Federation
    :return: The current exchange rate of the Central Bank of the Russian Federation
    """
    try:
        response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
        data = ET.fromstring(response.text)
        del response
        for course_item in data.findall("Valute"):
            if course_item.find("CharCode").text == "USD":
                return float(course_item.find("Value").text.replace(",", "."))
        logging.critical("Cannot get new course")
        return course
    except Exception as ex:
        logging.critical(f"Cannot get new course. {ex}")
        return course



def update_course() -> None:
    """
    Updating the rate in the environment relative to the current rate of the Central Bank of the Russian Federation
    :return:
    """
    course = get_new_course()
    with open(Path(Path.cwd(), "config", "course.json"), 'w') as file:
        json.dump({"course": course}, file, indent = 4)
    update_rubles_sum()


def update_rubles_sum() -> None:
    """
    The function of updating all amounts in rubles relative to the current exchange rate
    :return:
    """
    try:
        db.session.query(Order).filter().update({"price_rubles": Order.price_dollars * course})
        db.session.commit()
    except Exception as ex:
        logging.warning(f"Cannot update rubles courses due error: {ex}")
