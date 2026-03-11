import requests
from bs4 import BeautifulSoup
from .base import BaseCollector


class TikTokCreativeCenterCollector(BaseCollector):

    def __init__(self):
        super().__init__("tiktok_creative_center")

    def collect(self):
        url = "https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        ads = []

        try:
            response = requests.get(url, headers=headers, timeout=20)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                title = soup.title.string.strip() if soup.title and soup.title.string else "TikTok Top Ads"

                ad = {
                    "platform": "tiktok",
                    "country": "global",
                    "language": "en",
                    "headline": title,
                    "landing_url": url,
                    "active_ads_count": 50
                }

                ads.append(ad)

            print("\nTikTok ads coletados:\n")
            for ad in ads:
                print(ad)

        except Exception as e:
            print("Erro no coletor TikTok:", e)

        return ads

