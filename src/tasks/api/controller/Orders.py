from .. import exceptions
from ..datamapper import DataMapper
from flask import Blueprint, request
from ..model.Order import Order as OrderModel
from ..model.Orders import Orders as OrdersModel

orders_bp = Blueprint('orders_bp', __name__)


@orders_bp.route('/create', methods=['POST'])
def add_order():
    try:
        order = OrderModel.from_json(request.json)
        order_id = OrdersModel(DataMapper()).add_order(order)
        return {"order_id": order_id}
    except exceptions.InvalidAccount:
        return "Invalid account id", 400
    except exceptions.EmptyOrder:
        return "Empty order", 400
    except exceptions.BadOrderItemQuantity:
        return "Invalid order item quantity", 400
    except exceptions.OrderExists:
        return "Order already exists", 400


@orders_bp.route('/cancel', methods=['POST'])
def cancel_orders():
    account_numbers = request.json
    count = OrdersModel(DataMapper()).cancel_orders(account_numbers)
    return {"count": count}
