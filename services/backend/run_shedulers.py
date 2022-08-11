import json
import os
from celery import Celery
from celery.schedules import crontab

from backend.exchange import update_course
from backend.update_data import update_data
from backend.telegram_notifications import send_notifications_of_overdue_orders

from pathlib import Path
CELERY_BROKEN_URL = os.getenv("CELERY_BROKEN_URL", "sqlite://")
app = Celery(broker = "redis://redis:6379/1")

app.conf.timezone = 'Europe/Moscow'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, update_data_task.s(), name = 'Update data from tables')
    sender.add_periodic_task(crontab(hour = 0, minute = 0), update_course_task.s(),
                             name = "Update courses from Central Bank of the "
                                    "Russian Federation")
    sender.add_periodic_task(crontab(hour = 0, minute = 0), overdue_order_notifications.s(),
                             name = "Send notifications about overdue orders")

@app.task
def update_data_task():
    """
    Scheduler for update data from Google Sheets
    :return:
    """
    with open(Path(Path.cwd(), "config", "config.json"), 'r') as file:
        config_data = json.load(file)
    for table_key in config_data['orders_tables_keys']:
        update_data(table_key)


@app.task
def update_course_task():
    """
    Scheduler for update course from Central Bank of the Russian Federation
    :return:
    """
    #print("Update courses from Central Bank of the Russian Federation")
    #update_course()


@app.task
def overdue_order_notifications():
    """
    Scheduler for send notifications about overdue orders
    :return:
    """
    send_notifications_of_overdue_orders()
