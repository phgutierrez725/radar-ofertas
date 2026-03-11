from .base import BaseCollector


class MockAdsCollector(BaseCollector):

    def __init__(self):
        super().__init__("mock_ads")

    def collect(self):

        ads = [
            {
                "platform": "tiktok",
                "country": "ES",
                "language": "es",
                "headline": "Gana dinero con casino online",
                "landing_url": "https://casino-example.com",
                "active_ads_count": 25
            },
            {
                "platform": "facebook",
                "country": "BR",
                "language": "pt",
                "headline": "Ganhe dinheiro com apostas esportivas",
                "landing_url": "https://bet-example.com",
                "active_ads_count": 67
            },
            {
                "platform": "tiktok",
                "country": "UK",
                "language": "en",
                "headline": "Best betting app bonus today",
                "landing_url": "https://betbonus-example.com",
                "active_ads_count": 143
            },
            {
                "platform": "facebook",
                "country": "ES",
                "language": "es",
                "headline": "Pierde peso rápido con suplemento natural",
                "landing_url": "https://nutra-example.com",
                "active_ads_count": 120
            }
        ]

        print("Anúncios coletados:\n")

        for ad in ads:
            print(ad)

        return ads
