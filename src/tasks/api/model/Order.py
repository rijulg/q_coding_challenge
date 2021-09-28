from typing import List
from .. import exceptions
from hashlib import sha256
from base64 import b64encode
from datetime import datetime
from .OrderItem import OrderItem
from dataclasses import dataclass
from .OrderStatus import OrderStatus


@dataclass
class Order:
    account_number: str
    status: OrderStatus
    timestamp: datetime
    items: List[OrderItem]

    def hash(self):
        data = repr(self).encode('utf8')
        h = sha256(data).digest()
        return b64encode(h)

    @staticmethod
    def from_json(data):
        if len(data["items"]) == 0:
            raise exceptions.EmptyOrder()
        items = []
        for item in data["items"]:
            product_id = item['product_id']
            quantity = item['quantity']
            if quantity < 1:
                raise exceptions.BadOrderItemQuantity()
            items += [OrderItem(product_id, quantity)]

        return Order(
            data["account_number"],
            OrderStatus.Active,
            datetime.fromtimestamp(data["timestamp"]),
            items
        )
