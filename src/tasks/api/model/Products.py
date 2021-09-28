from ..datamapper import DataMapper


class Products:

    def __init__(self, datamapper: DataMapper) -> None:
        self.__datamapper = datamapper

    def top_selling(self, num_items):
        return self.__datamapper.top_selling_items(num_items)
