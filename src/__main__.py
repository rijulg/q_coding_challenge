import argparse
from .tasks.sql import Task as SqlTask
from .tasks.api import Task as ApiTask
from .tasks.api import API as API


tasks = {
    "sql": SqlTask,
    "api": ApiTask,
    "api2": API,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model")
    parser.add_argument(
        "task",
        choices=tasks.keys()
    )
    task = tasks[parser.parse_args().task]
    task().run()
