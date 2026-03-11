class NicheClassifier:
    IGAMING_KEYWORDS = [
        # inglês
        "casino",
        "online casino",
        "bet",
        "bets",
        "betting",
        "sports betting",
        "sportsbook",
        "bookmaker",
        "bookmakers",
        "slot",
        "slots",
        "roulette",
        "blackjack",
        "poker",
        "jackpot",
        "free spins",
        "welcome bonus",
        "deposit bonus",
        "sign up bonus",
        "bet now",
        "place your bet",
        "gambling",

        # português
        "cassino",
        "casino online",
        "aposta",
        "apostas",
        "apostas esportivas",
        "casa de aposta",
        "casas de apostas",
        "slot",
        "slots",
        "roleta",
        "blackjack",
        "poker",
        "jackpot",
        "giros grátis",
        "rodadas grátis",
        "bonus de boas-vindas",
        "bônus de boas-vindas",
        "bonus de deposito",
        "bônus de depósito",
        "cadastre-se e ganhe",
        "deposite e ganhe",
        "aposte agora",

        # espanhol / LATAM
        "casino en linea",
        "casino online",
        "casino",
        "apuesta",
        "apuestas",
        "apuestas deportivas",
        "casa de apuestas",
        "slot",
        "slots",
        "ruleta",
        "blackjack",
        "poker",
        "jackpot",
        "giros gratis",
        "tiradas gratis",
        "bono de bienvenida",
        "bono por deposito",
        "bono por depósito",
        "registrate y gana",
        "regístrate y gana",
        "deposita y gana",
        "apuesta ahora",
        "tragamonedas",
        "pronosticos deportivos",
        "pronósticos deportivos"
    ]

    def classify(self, text: str) -> str:
        if not text:
            return "unknown"

        lower_text = text.lower()

        for keyword in self.IGAMING_KEYWORDS:
            if keyword in lower_text:
                return "igaming"

        return "other"
