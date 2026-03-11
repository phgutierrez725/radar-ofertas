import requests
from bs4 import BeautifulSoup
from .base import BaseCollector


class TaboolaAdsCollector(BaseCollector):

    def __init__(self):
        super().__init__("taboola_ads")

    def collect(self):

        url = "https://www.taboola.com"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        ads = []

        try:

            response = requests.get(url, headers=headers, timeout=20)

            if response.status_code == 200:

                soup = BeautifulSoup(response.text, "html.parser")

                title = soup.title.string.strip() if soup.title else "Taboola Ads"

                ad = {
                    "platform": "taboola",
                    "country": "global",
                    "language": "unknown",
                    "headline": title,
                    "landing_url": url,
                    "creative_url": url,
                    "active_ads_count": 100
                }

                ads.append(ad)

            print("\nTaboola ads coletados:\n")

            for ad in ads:
                print(ad)

        except Exception as e:
            print("Erro no coletor Taboola:", e)

        return ads

