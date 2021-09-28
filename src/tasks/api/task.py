from .api import api
from datetime import datetime


class Task:

    @property
    def app_client(self):
        with api.app_context():
            with api.test_client() as client:
                return client

    def run(self):
        self.__add_order_invalid_account()
        self.__add_order_empty_order()
        self.__add_order_bad_item_quantity()
        self.__add_order_duplicate()
        self.__add_order_success()
        self.__top_three_selling()
        self.__recent_customers()
        self.__cancel_orders()

    def __add_order_invalid_account(self):
        print("Add order invalid id:: ")
        res = self.app_client.post(
            '/orders/create',
            json={
                "account_number": "hacker_man",
                "timestamp": int(datetime.now().timestamp()),
                "items": [
                    {
                        "product_id": "prod_00001",
                        "quantity": 2
                    }
                ]
            }
        )
        print(res.status, res.data)

    def __add_order_empty_order(self):
        print("Add order empty order:: ")
        res = self.app_client.post(
            '/orders/create',
            json={
                "account_number": "acct_00003",
                "timestamp": int(datetime.now().timestamp()),
                "items": []
            }
        )
        print(res.status, res.data)

    def __add_order_bad_item_quantity(self):
        print("Add order bad item quantity:: ")
        res = self.app_client.post(
            '/orders/create',
            json={
                "account_number": "acct_00003",
                "timestamp": int(datetime.now().timestamp()),
                "items": [
                    {
                        "product_id": "prod_00001",
                        "quantity": -1
                    }
                ]
            }
        )
        print(res.status, res.data)
        res = self.app_client.post(
            '/orders/create',
            json={
                "account_number": "acct_00003",
                "timestamp": int(datetime.now().timestamp()),
                "items": [
                    {
                        "product_id": "prod_00001",
                        "quantity": 0
                    }
                ]
            }
        )
        print(res.status, res.data)

    def __add_order_duplicate(self):
        print("Add order duplicate:: ")
        res = self.app_client.post(
            '/orders/create',
            json={
                "account_number": "acct_00003",
                "timestamp": 123456789,
                "items": [
                    {
                        "product_id": "prod_00001",
                        "quantity": 1
                    }
                ]
            }
        )
        print(res.status, res.data)

    def __add_order_success(self):
        print("Add order success:: ")
        res = self.app_client.post(
            '/orders/create',
            json={
                "account_number": "acct_00001",
                "timestamp": int(datetime.now().timestamp()),
                "items": [
                    {
                        "product_id": "prod_00001",
                        "quantity": 2
                    },
                    {
                        "product_id": "prod_00002",
                        "quantity": 2
                    }
                ]
            }
        )
        print(res.status, res.data)

    def __top_three_selling(self):
        print("Top three selling:: ")
        res = self.app_client.get('/products/top_selling/3')
        print(res.status, res.data)

    def __recent_customers(self):
        print("Recent customers in last 3 days:: ")
        res = self.app_client.get('/customers/count_recent/3')
        print(res.status, res.data)

    def __cancel_orders(self):
        print("Cancel orders of [account acct_00001, acct_0002]:: ")
        res = self.app_client.post(
            '/orders/cancel',
            json=['acct_00001', 'acct_00002']
        )
        print(res.status, res.data)
