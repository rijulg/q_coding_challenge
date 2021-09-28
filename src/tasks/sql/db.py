import mysql.connector


class DB:

    __tables = {
        "MEMBER_DETAILS": """
            CREATE TABLE MEMBER_DETAILS(
                ACCT_NUMBER CHAR(10),
                JOIN_DATE DATE
            )
        """,
        "MEMBER_EARN": """
            CREATE TABLE MEMBER_EARN(
                ACCT_NUMBER CHAR(10),
                EARN_TYPE_CODE INT,
                EARN_TIMESTAMP TIMESTAMP,
                EARN_VALUE INT
            )
        """,
        "EARN_TYPE": """
            CREATE TABLE EARN_TYPE(
                EARN_TYPE_CODE INT,
                EARN_TYPE_NAME VARCHAR(255)
            )
        """,
    }

    __mock_data = [
        "INSERT INTO EARN_TYPE VALUES(0, 'TRAVEL - 1')",
        "INSERT INTO EARN_TYPE VALUES(1, 'TRAVEL - 2')",
        "INSERT INTO EARN_TYPE VALUES(2, 'TRAVEL - 3')",
        "INSERT INTO EARN_TYPE VALUES(3, 'SHOPPING')",
        "INSERT INTO EARN_TYPE VALUES(4, 'GIFT')",

        "INSERT INTO MEMBER_DETAILS VALUES('acct_00001', curdate() - interval 13 day)",
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00001', curdate() - interval 12 day)",
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00001', curdate() - interval 11 day)",
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00002', curdate() - interval 10 day)",
        "INSERT INTO MEMBER_DETAILS VALUES('acct_00003', curdate() - interval 09 day)",

        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 0, curdate(), 1)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 0, curdate(), 10)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 0, curdate(), 2)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 1, curdate(), 2)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 2, curdate(), 3)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 3, curdate(), 4)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00001', 4, curdate(), 5)",

        "INSERT INTO MEMBER_EARN VALUES('acct_00002', 0, curdate(), 1)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00002', 1, curdate(), 2)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00002', 2, curdate(), 3)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00002', 3, curdate(), 4)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00002', 4, curdate(), 5)",

        "INSERT INTO MEMBER_EARN VALUES('acct_00003', 0, curdate(), 1)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00003', 1, curdate(), 2)",
        "INSERT INTO MEMBER_EARN VALUES('acct_00003', 4, curdate(), 5)",

    ]

    def __init__(self) -> None:
        self.__connection = mysql.connector.connect(
            user='sql_task',
            password='sql_task',
            host='localhost',
            database='sql_task'
        )
        self.__delete_tables()
        self.__create_tables()
        self.__setup_mock_data()

    def __del__(self) -> None:
        self.__delete_tables()
        self.__connection.close()

    def __create_tables(self):
        cursor = self.__connection.cursor()
        for table_desc in self.__tables.values():
            cursor.execute(table_desc)
        cursor.close()

    def __delete_tables(self):
        cursor = self.__connection.cursor()
        for table_name in self.__tables.keys():
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.close()

    def __setup_mock_data(self):
        cursor = self.__connection.cursor()
        for data in self.__mock_data:
            cursor.execute(data)
        self.__connection.commit()
        cursor.close()

    def raw_query(self, query):
        cursor = self.__connection.cursor()
        cursor.execute(query)
        result = list(cursor)
        cursor.close()
        return result
