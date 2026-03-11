import requests
from bs4 import BeautifulSoup
from .base import BaseCollector


class GoogleAdsCollector(BaseCollector):

    def __init__(self):
        super().__init__("google_ads")

    def collect(self):

        url = "https://adstransparency.google.com"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        ads = []

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string if soup.title else "Google Ads"

            ad = {
                "platform": "google",
                "headline": title,
                "landing_url": url
            }

            ads.append(ad)

        print("\nGoogle Ads coletados:")
        for ad in ads:
            print(ad)

        return ads
