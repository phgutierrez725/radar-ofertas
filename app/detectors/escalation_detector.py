import json
import os


class EscalationDetector:

    def __init__(self):

        self.file_path = "data/ad_history.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

        with open(self.file_path, "r") as f:
            self.history = json.load(f)

    def check(self, ad_id, active_ads_count):

        previous = self.history.get(ad_id)

        self.history[ad_id] = active_ads_count

        with open(self.file_path, "w") as f:
            json.dump(self.history, f, indent=2)

        if previous is None:
            return False

        if active_ads_count >= previous * 2 and active_ads_count > 50:
            return True

        return False
