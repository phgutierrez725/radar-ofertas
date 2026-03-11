import json
import os


class NewLandingDetector:

    def __init__(self):
        self.file_path = "data/known_landings.json"

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

        with open(self.file_path, "r") as f:
            self.known_landings = json.load(f)

    def check(self, landing_url):

        if landing_url not in self.known_landings:

            self.known_landings.append(landing_url)

            with open(self.file_path, "w") as f:
                json.dump(self.known_landings, f, indent=2)

            return True

        return False

