import json
import logging
from datetime import datetime as dt
from backend.dbModels.order import Order
from backend.dbModels.order import db
from telebot import TeleBot
from pathlib import Path

from sqlalchemy import and_


def send_notification(message_data: Order | str) -> None:
    """
    The function of sending a notification on an overdue order
    :param message_data: Expired order model or message to send
    :return:
    """
    with open(Path(Path.cwd(), "config", "config.json"), 'r') as file:
        config_data = json.load(file)
    telegram_bot = TeleBot(config_data['telegram_bot_token'])
    if type(message_data) == Order:
        message_to_send = f"Expired order {message_data}"
    else:
        message_to_send = message_data
    for telegram_user_for_notification in config_data['telegram_users_for_notifications']:
        try:
            telegram_bot.send_message(telegram_user_for_notification, message_to_send)
        except Exception as ex:
            logging.warning(f"Cannot send notification to user {telegram_user_for_notification} by order "
                            f"{message_data.order_id}. {ex}")


def send_notifications_of_overdue_orders() -> int:
    """
    Function to receive expired orders and start sending notifications on them
    :return: Number of notifications sent
    """
    today = dt.now().date()
    count_notifications = 0
    for order in db.session.query(Order).filter(and_(Order.delivery_time < today, Order.notification_is_send == False)):
        count_notifications += 1
        send_notification(order)
        order.notification_is_send = True
    db.session.commit()
    return count_notifications
