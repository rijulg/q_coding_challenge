import datetime
import mysql.connector
from .model.Order import Order
from .model.OrderItem import OrderItem
from .model.OrderStatus import OrderStatus


class PrefilledDB:

    __tables = {
        "MEMBER_DETAILS": """
            CREATE TABLE MEMBER_DETAILS(
                ACCOUNT_NUMBER CHAR(10),
                JOIN_DATE DATE
            )
        """,
        "PRODUCT_DETAILS": """
            CREATE TABLE PRODUCT_DETAILS(
                PRODUCT_NAME VARCHAR(256),
                VALUE DECIMAL
            )
        """,
        "ORDER_DETAILS": """
            CREATE TABLE ORDER_DETAILS(
                ORDER_ID CHAR(10),
                ACCOUNT_NUMBER CHAR(10),
                ORDER_TIME TIMESTAMP,
                ORDER_STATUS ENUM('ACTIVE', 'CANCELLED'),
                ORDER_HASH CHAR(64)
            )
        """,
        "ORDER_ITEMS": """
            CREATE TABLE ORDER_ITEMS(
                ORDER_ID CHAR(10),
                PRODUCT_NAME VARCHAR(256),
                QUANTITY INT UNSIGNED
            )
        """,
    }

    __mock_data = [
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00001', curdate() - interval 13 day)",
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00002', curdate() - interval 10 day)",
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00003', curdate() - interval 09 day)",

        "INSERT INTO PRODUCT_DETAILS VALUES('prod_00001', 1000)",
        "INSERT INTO PRODUCT_DETAILS VALUES('prod_00002', 2000)",
        "INSERT INTO PRODUCT_DETAILS VALUES('prod_00003', 3000)",
    ]
    __mock_orders = [
        Order(
            "acct_00001",
            OrderStatus.Cancelled,
            datetime.datetime.now(),
            [
                OrderItem("prod_00001", 1),
                OrderItem("prod_00002", 2),
                OrderItem("prod_00003", 3),
            ]
        ),
        Order(
            "acct_00001",
            OrderStatus.Active,
            datetime.datetime.now(),
            [
                OrderItem("prod_00001", 4),
                OrderItem("prod_00002", 2),
                OrderItem("prod_00003", 4),
            ]
        ),
        Order(
            "acct_00002",
            OrderStatus.Active,
            datetime.datetime.now(),
            [
                OrderItem("prod_00001", 1),
                OrderItem("prod_00002", 2),
            ]
        ),
        Order(
            "acct_00003",
            OrderStatus.Active,
            datetime.datetime.now(),
            [
                OrderItem("prod_00001", 1),
            ]
        ),
        Order(
            "acct_00003",
            OrderStatus.Active,
            datetime.datetime.fromtimestamp(123456789),
            [
                OrderItem("prod_00001", 1),
            ]
        )
    ]

    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            user='api_task',
            password='api_task',
            host='localhost',
            database='api_task'
        )
        self.__delete_tables()
        self.__create_tables()
        self.__setup_mock_data()

    def __del__(self) -> None:
        self.__delete_tables()
        self.connection.close()

    def __create_tables(self):
        cursor = self.connection.cursor()
        for table_desc in self.__tables.values():
            cursor.execute(table_desc)
        cursor.close()

    def __delete_tables(self):
        cursor = self.connection.cursor()
        for table_name in self.__tables.keys():
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.close()

    def __setup_mock_data(self):
        cursor = self.connection.cursor()
        for data in self.__mock_data:
            cursor.execute(data)
        self.connection.commit()
        cursor.close()
        for order in self.__mock_orders:
            self.add_order(order)


class DataMapper(PrefilledDB):

    __order_counter = 0

    def __init__(self) -> None:
        super().__init__()

    def account_exists(self, account_number: str) -> bool:
        cursor = self.connection.cursor()
        prepared_statement = "SELECT ACCOUNT_NUMBER FROM MEMBER_DETAILS WHERE ACCOUNT_NUMBER=%s"
        cursor.execute(prepared_statement, (account_number,))
        list(cursor)
        order_exists = cursor.rowcount == 1
        cursor.close()
        return order_exists

    def order_hash_exists(self, order_hash: str) -> bool:
        cursor = self.connection.cursor()
        prepared_statement = "SELECT ORDER_ID FROM ORDER_DETAILS WHERE ORDER_HASH=%s"
        cursor.execute(prepared_statement, (order_hash,))
        list(cursor)
        order_exists = cursor.rowcount == 1
        cursor.close()
        return order_exists

    def add_order(self, order: Order):
        order_id = f"ordr_{self.__order_counter:04}"
        self.__order_counter += 1
        cursor = self.connection.cursor()
        prepared_statement = "INSERT INTO ORDER_DETAILS VALUES(%s, %s, %s, %s, %s)"
        data = (order_id, order.account_number,
                order.timestamp, order.status, order.hash())
        cursor.execute(prepared_statement, data)
        prepared_statement = "INSERT INTO ORDER_ITEMS VALUE(%s, %s, %s)"
        for item in order.items:
            data = (order_id, item.product_id, item.quantity)
            cursor.execute(prepared_statement, data)
        self.connection.commit()
        cursor.close()
        return order_id

    def top_selling_items(self, num_items):
        cursor = self.connection.cursor()
        best_seller_query = """
            SELECT
                PRODUCT_NAME,
                SUM(QUANTITY) AS TOTAL_QUANTITY
            FROM ORDER_ITEMS
            GROUP BY PRODUCT_NAME
            ORDER BY TOTAL_QUANTITY DESC
            LIMIT %s
        """
        prepared_statement = f"""
            SELECT
                BEST_SELLER.PRODUCT_NAME,
                BEST_SELLER.TOTAL_QUANTITY * PRODUCT_DETAILS.VALUE
            FROM
                ({best_seller_query}) as BEST_SELLER
                INNER JOIN PRODUCT_DETAILS
                ON
                    BEST_SELLER.PRODUCT_NAME = PRODUCT_DETAILS.PRODUCT_NAME
        """
        cursor.execute(prepared_statement, (num_items,))
        items = list(cursor)
        cursor.close()
        return items

    def count_recent_customers(self, num_days):
        cursor = self.connection.cursor()
        prepared_statement = f"""
            SELECT
                COUNT(DISTINCT ACCOUNT_NUMBER)
            FROM
                ORDER_DETAILS
            WHERE
                DATEDIFF(CURDATE(), ORDER_DETAILS.ORDER_TIME) < %s
        """
        cursor.execute(prepared_statement, (num_days,))
        num_customers = next(cursor)[0]
        cursor.close()
        return num_customers

    def cancel_orders(self, account_numbers):
        cursor = self.connection.cursor()
        prepared_statement = f"""
            UPDATE
                ORDER_DETAILS
            SET
                ORDER_STATUS = "CANCELLED"
            WHERE
                ACCOUNT_NUMBER IN ({', '.join(['%s'] * len(account_numbers))})
        """
        cursor.execute(prepared_statement, tuple(account_numbers))
        cancel_count = cursor.rowcount
        cursor.close()
        return cancel_count
