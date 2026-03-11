import json
import os

class NewCreativeDetector:

    def __init__(self):
        self.file_path = "data/known_creatives.json"

        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

        with open(self.file_path, "r") as f:
            self.known_creatives = json.load(f)

    def check(self, creative_url):

        if creative_url not in self.known_creatives:

            self.known_creatives.append(creative_url)

            with open(self.file_path, "w") as f:
                json.dump(self.known_creatives, f, indent=2)

            return True

        return False

