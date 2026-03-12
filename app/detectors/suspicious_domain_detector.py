from urllib.parse import urlparse


class SuspiciousDomainDetector:
    def __init__(self):
        self.suspicious_tlds = [
            ".vip",
            ".pro",
            ".app",
            ".shop",
            ".site",
            ".online",
            ".live",
            ".click",
            ".fun",
            ".trade"
        ]

    def extract_domain(self, url):
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except Exception:
            return ""

    def check(self, landing_url):
        domain = self.extract_domain(landing_url)

        if not domain:
            return False

        for tld in self.suspicious_tlds:
            if domain.endswith(tld):
                return True

        return False
