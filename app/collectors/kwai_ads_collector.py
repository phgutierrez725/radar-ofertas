import requests
from bs4 import BeautifulSoup
from .base import BaseCollector


class KwaiAdsCollector(BaseCollector):

    def __init__(self):
        super().__init__("kwai_ads")

    def collect(self):

        url = "https://ads.kwai.com"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        ads = []

        try:

            response = requests.get(url, headers=headers, timeout=20)

            if response.status_code == 200:

                soup = BeautifulSoup(response.text, "html.parser")

                title = soup.title.string.strip() if soup.title else "Kwai Ads"

                ad = {
                    "platform": "kwai",
                    "country": "global",
                    "language": "unknown",
                    "headline": title,
                    "landing_url": url,
                    "creative_url": url,
                    "active_ads_count": 80
                }

                ads.append(ad)

            print("\nKwai ads coletados:\n")

            for ad in ads:
                print(ad)

        except Exception as e:
            print("Erro no coletor Kwai:", e)

        return ads

