from .Order import Order
from .. import exceptions
from ..datamapper import DataMapper


class Orders:

    def __init__(self, datamapper: DataMapper) -> None:
        self.__datamapper = datamapper

    def add_order(self, order: Order) -> str:
        if not self.__datamapper.account_exists(order.account_number):
            raise exceptions.InvalidAccount()
        if self.__datamapper.order_hash_exists(order.hash()):
            raise exceptions.OrderExists()
        return self.__datamapper.add_order(order)

    def cancel_orders(self, account_numbers) -> int:
        return self.__datamapper.cancel_orders(account_numbers)
