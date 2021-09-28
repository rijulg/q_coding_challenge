from ..datamapper import DataMapper


class Customers:

    def __init__(self, datamapper: DataMapper) -> None:
        self.__datamapper = datamapper

    def count_recent(self, num_days: int) -> int:
        return self.__datamapper.count_recent_customers(num_days)
