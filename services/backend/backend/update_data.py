import pygsheets
import logging
from datetime import datetime as dt
from pathlib import Path
from backend.dbModels.order import Order
from backend.dbModels.order import db
from backend.exchange import dollars_to_rubles


def get_data_dict_from_table(table_key: str) -> list[dict]:
    """
    The function allows you to get data from Google Sheets using a given api key in the config folder
    :param table_key: Table key from Google Sheets
    :return: List of dictionaries with values and keys from a table
    """
    try:
        client = pygsheets.authorize(service_file = Path(Path.cwd(), "config", "sheets_api_key.json"))
        table = client.open_by_key(table_key)
        sheet = table.sheet1
        records = sheet.get_all_records()
        return records
    except Exception as ex:
        logging.error(f"Cannot get table {table_key} {ex}")
    return []


def update_data(table_key: str) -> None:
    """
    The function of updating data to a local database from a Google Sheets table
    :param table_key: Table key from Google Sheets
    """
    rows = get_data_dict_from_table(table_key)
    orders_ids = []
    for row in rows:
        try:
            order = Order(id = row['№'],
                          order_id = row['заказ №'],
                          price_dollars = row['стоимость,$'],
                          price_rubles = dollars_to_rubles(row['стоимость,$']),
                          delivery_time = dt.strptime(row['срок поставки'], "%d.%m.%Y").date())
            orders_ids.append(row['заказ №'])
        except Exception as ex:
            logging.warning(f"Cannot add order {row} {ex}")
    orders_ids = tuple(orders_ids)
    try:
        db.session.query(Order).filter(Order.order_id.not_in(orders_ids)).delete()
    except Exception as ex:
        logging.warning(f"Cannot delete orders due error {ex}")
    db.session.commit()
