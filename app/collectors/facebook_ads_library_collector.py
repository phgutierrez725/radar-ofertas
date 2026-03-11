import requests
from bs4 import BeautifulSoup
from .base import BaseCollector


class FacebookAdsLibraryCollector(BaseCollector):
    def __init__(self):
        super().__init__("facebook_ads_library")

    def collect(self):
        url = "https://www.facebook.com/ads/library/"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        ads = []

        try:
            response = requests.get(url, headers=headers, timeout=20)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                title = (
                    soup.title.string.strip()
                    if soup.title and soup.title.string
                    else "Meta Ads Library"
                )

                ad = {
                    "platform": "facebook",
                    "country": "global",
                    "language": "unknown",
                    "headline": title,
                    "landing_url": url,
                    "creative_url": url,
                    "active_ads_count": 120
                }

                ads.append(ad)

            print("\nFacebook ads coletados:\n")
            for ad in ads:
                print(ad)

        except Exception as e:
            print("Erro no coletor Facebook:", e)

        return ads

