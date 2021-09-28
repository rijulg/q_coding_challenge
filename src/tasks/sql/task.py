from .db import DB


class Task:
    __db = DB()

    def run(self):
        print("Executing SQL Task")
        self.__q1()
        self.__q2()
        self.__q3()
        self.__q4()
        self.__q5()
        self.__q6()

    def __q1(self):
        print("Q1:: ")
        query = """
            SELECT
                MEMBER_EARN.ACCT_NUMBER,
                DATE(MEMBER_EARN.EARN_TIMESTAMP),
                MEMBER_EARN.EARN_TYPE_CODE,
                MEMBER_EARN.EARN_VALUE
            FROM
                MEMBER_DETAILS INNER JOIN MEMBER_EARN
                ON MEMBER_DETAILS.ACCT_NUMBER = MEMBER_EARN.ACCT_NUMBER
            WHERE
                DATEDIFF(MEMBER_EARN.EARN_TIMESTAMP, MEMBER_DETAILS.JOIN_DATE) < 10
        """
        result = self.__db.raw_query(query)
        for res in result:
            print(res)

    def __q2(self):
        print("Q2:: ")
        viewname = "UNIQUE_EARNS"
        self.__db.raw_query(
            f"DROP VIEW IF EXISTS {viewname}"
        )

        query = f"""
            CREATE VIEW {viewname} AS
            SELECT
                EARN_TYPE.EARN_TYPE_NAME AS EARN_TYPE_NAME,
                COUNT(DISTINCT MEMBER_EARN.ACCT_NUMBER) AS UNIQUE_MEMBERS
            FROM
                MEMBER_EARN INNER JOIN EARN_TYPE
                ON MEMBER_EARN.EARN_TYPE_CODE = EARN_TYPE.EARN_TYPE_CODE
            GROUP BY
                EARN_TYPE.EARN_TYPE_NAME
        """
        self.__db.raw_query(query)

        for res in self.__db.raw_query(
            f"SELECT * FROM {viewname}"
        ):
            print(res)

    def __q3(self):
        print("Q3:: ")
        viewname = "UNIQUE_EARNS"
        self.__db.raw_query(
            f"DROP VIEW IF EXISTS {viewname}"
        )
        query = f"""
            CREATE VIEW {viewname} AS
            SELECT
                EARN_TYPE.EARN_TYPE_NAME AS EARN_TYPE_NAME,
                COUNT(DISTINCT MEMBER_EARN.ACCT_NUMBER) AS UNIQUE_MEMBERS
            FROM
                MEMBER_EARN INNER JOIN EARN_TYPE
                ON MEMBER_EARN.EARN_TYPE_CODE = EARN_TYPE.EARN_TYPE_CODE
            GROUP BY
                EARN_TYPE.EARN_TYPE_NAME
        """
        self.__db.raw_query(query)

        query = f"""
            SELECT EARN_TYPE_NAME
            FROM {viewname}
            ORDER BY UNIQUE_MEMBERS
            LIMIT 1
            OFFSET 2
        """
        result = self.__db.raw_query(query)
        for res in result:
            print(res)

    def __q4(self):
        print("Q4:: ")

        query = f"""
            SELECT
                EARN_TYPE.EARN_TYPE_NAME AS EARN_TYPE_NAME,
                AVG(MEMBER_EARN.EARN_VALUE) AS AVG_EARN
            FROM
                MEMBER_EARN INNER JOIN EARN_TYPE
                ON MEMBER_EARN.EARN_TYPE_CODE = EARN_TYPE.EARN_TYPE_CODE
            WHERE
                EARN_TYPE.EARN_TYPE_NAME LIKE "TRAVEL%"
            GROUP BY
                EARN_TYPE.EARN_TYPE_NAME
            ORDER BY
                AVG_EARN DESC
        """
        result = self.__db.raw_query(query)

        for res in result:
            print(res)

    def __q5(self):
        print("Q5:: ")

        usually_high_query = f"""
            SELECT
                EARN_TYPE.EARN_TYPE_CODE,
                EARN_TYPE.EARN_TYPE_NAME,
                (AVG(MEMBER_EARN.EARN_VALUE) + STDDEV(MEMBER_EARN.EARN_VALUE)) AS USUALLY_HIGH
            FROM
                MEMBER_EARN INNER JOIN EARN_TYPE
                ON MEMBER_EARN.EARN_TYPE_CODE = EARN_TYPE.EARN_TYPE_CODE
            GROUP BY
                EARN_TYPE.EARN_TYPE_CODE, EARN_TYPE.EARN_TYPE_NAME
        """
        query = f"""
            SELECT
                MEMBER_EARN.ACCT_NUMBER,
                UHQ.EARN_TYPE_NAME
            FROM
                MEMBER_EARN LEFT JOIN ({usually_high_query}) AS UHQ
                ON
                    MEMBER_EARN.EARN_TYPE_CODE = UHQ.EARN_TYPE_CODE
            WHERE
                MEMBER_EARN.EARN_VALUE > UHQ.USUALLY_HIGH
        """
        result = self.__db.raw_query(query)

        for res in result:
            print(res)

    def __q6(self):
        print("Q6:: ")
        min_date_query = """
        SELECT
            ACCT_NUMBER,
            MIN(JOIN_DATE) AS MIN_DATE
        FROM
            MEMBER_DETAILS
        GROUP BY
            ACCT_NUMBER
        """
        query = f"""
            DELETE MEMBER_DETAILS
            FROM
                MEMBER_DETAILS LEFT JOIN ({min_date_query}) AS MIN_DATE
                ON
                    MEMBER_DETAILS.ACCT_NUMBER = MIN_DATE.ACCT_NUMBER
            WHERE
                MEMBER_DETAILS.JOIN_DATE > MIN_DATE.MIN_DATE
        """
        result = self.__db.raw_query(query)
        for res in result:
            print(res)

        query = """SELECT * FROM MEMBER_DETAILS;"""
        result = self.__db.raw_query(query)
        for res in result:
            print(res)
