class ScoreEngine:
    def calculate_score(self, ad: dict) -> dict:
        score = 0
        reasons = []

        niche = ad.get("niche", "unknown")
        language = ad.get("detected_language", "unknown")
        headline = (ad.get("headline") or "").lower()
        platform = ad.get("platform", "unknown")
        active_ads_count = ad.get("active_ads_count", 0)

        if niche == "igaming":
            score += 4
            reasons.append("nicho igaming detectado")

        if language in ["pt", "es", "en"]:
            score += 2
            reasons.append("idioma alvo detectado")

        strong_terms = [
            "bonus", "bônus", "bono",
            "casino", "cassino",
            "bet", "aposta", "apuestas",
            "slot", "slots",
            "free spins", "giros gratis", "rodadas grátis"
        ]

        if any(term in headline for term in strong_terms):
            score += 2
            reasons.append("termos fortes de oferta detectados")

        if platform in ["tiktok", "facebook", "google"]:
            score += 1
            reasons.append("plataforma monitorada")

        if active_ads_count >= 20:
            score += 3
            reasons.append("20+ anúncios ativos")

        if active_ads_count >= 50:
            score += 2
            reasons.append("50+ anúncios ativos")

        if active_ads_count >= 100:
            score += 3
            reasons.append("100+ anúncios ativos")

        if score >= 12:
            status = "escalada"
        elif score >= 8:
            status = "forte"
        elif score >= 4:
            status = "promissora"
        else:
            status = "fraca"

        return {
            "score": score,
            "status": status,
            "reasons": reasons
        }
