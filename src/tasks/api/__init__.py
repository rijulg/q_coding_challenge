from .task import Task
from .api import api


class API:

    def run(self):
        api.debug = False
        api.run()
