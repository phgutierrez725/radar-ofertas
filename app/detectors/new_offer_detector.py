import json
import os
from urllib.parse import urlparse


class NewOfferDetector:

    def __init__(self):

        self.file_path = "data/known_domains.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file_path):

            with open(self.file_path, "w") as f:
                json.dump([], f)

        with open(self.file_path, "r") as f:
            self.known_domains = json.load(f)

    def extract_domain(self, url):

        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return None

    def check(self, landing_url):

        domain = self.extract_domain(landing_url)

        if not domain:
            return False

        if domain not in self.known_domains:

            self.known_domains.append(domain)

            with open(self.file_path, "w") as f:
                json.dump(self.known_domains, f, indent=2)

            return True

        return False
