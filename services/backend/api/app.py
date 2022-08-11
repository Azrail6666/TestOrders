import json
from app_init import app
from backend.dbModels.order import Order
from backend.dbModels.order import db
from flask import request

from sqlalchemy import func


@app.route("/")
def start():
    return "App run"

@app.route("/get_orders", methods = ["POST"])
def get_orders():
    """
    Function for getting a list of orders via API
    :return: JSON Response with order data
    """
    if request.form.get("page"):
        try:
            page = int(request.form.get("page"))
            limit = 20
            if request.form.get("limit"):
                limit = int(request.form.get("limit"))
            offset = limit * (page - 1)
            tmp_orders = db.session.query(Order).order_by(Order.id).limit(limit).offset(offset).all()
            orders = []
            for tmp_order in tmp_orders:
                orders.append(tmp_order.to_array())
            return {
                "status": True,
                "data": {
                    "ordersHead": [
                        "№",
                        "Заказ №",
                        "Cтоимость, $",
                        "Cтоимость, ₽",
                        "Срок Поставки"
                    ],
                    "orders": orders,
                    "total_count": db.session.query(Order).count()
                }
            }
        except Exception as ex:
            return json.dumps({
                "status": False,
                "error": f"Failed to get list of orders due to an error {ex}"
            })
    return json.dumps({
        "status": False,
        "error": "Cannot get list of orders because page number value was not given"
    })


@app.route("/get_days_statistic")
def get_days_statistic():
    """
    Function to get order statistics by day via API
    :return: Response with statistics by day
    """
    try:
        date_statistic_data = db.session.query(Order.delivery_time,
                                               func.count(Order.delivery_time)).group_by(Order.delivery_time).all()
        labels = []
        data = []
        for date_statistic_data_row in date_statistic_data:
            labels.append(date_statistic_data_row[0].strftime("%d-%m-%Y"))
            data.append(date_statistic_data_row[1])
        return json.dumps({
            "status": True,
            "data": {
                "labels": labels,
                "data": data
            }
        })
    except Exception as ex:
        return json.dumps({
            "status": False,
            "error": f"Failed to get days statistic of orders due to an error {ex}"
        })



def run_app():
    app.run()