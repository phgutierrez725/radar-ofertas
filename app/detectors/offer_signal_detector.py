class OfferSignalDetector:

    def __init__(self):

        self.offer_keywords = [

            "profit","lucro","ganancia",

            "earn","ganhar","ganar",

            "income","renda","ingresos",

            "money","dinheiro","dinero",

            "make money","ganhar dinheiro","ganar dinero",

            "passive income","renda passiva","ingresos pasivos",

            "crypto","cripto","bitcoin",

            "trading","robô de trading","bot de trading",

            "investment","investimento","inversión",

            "forex",

            "casino","cassino",

            "bet","aposta",

            "slots",

            "jackpot",

            "ai profit","lucro com ia","ganancias con ia",

            "ai trading","trading com ia","trading con ia",

            "system","sistema",

            "method","método"

        ]

    def check(self, headline):

        if not headline:
            return False

        headline = headline.lower()

        for keyword in self.offer_keywords:

            if keyword in headline:
                return True

        return False
