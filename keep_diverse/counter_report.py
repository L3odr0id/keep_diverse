from collections import Counter
import json


class CounterReport:
    def __init__(self, output_file_path: str):
        self.output_file_path = output_file_path

    def save(self, counter: Counter):
        with open(self.output_file_path, "w") as f:
            json.dump(dict(counter), f, indent=2)


class NoCounterReport:
    def __init__(self):
        pass

    def save(self, counter: Counter):
        pass
