import time

from app.collectors.mock_ads_collector import MockAdsCollector
from app.collectors.google_ads_collector import GoogleAdsCollector
from app.collectors.tiktok_creative_center_collector import TikTokCreativeCenterCollector

from app.classifiers.niche import NicheClassifier
from app.classifiers.language import LanguageDetector

from app.scoring.engine import ScoreEngine
from app.alerts.telegram_sender import send_telegram_message


INTERVAL_SECONDS = 1800  # 30 minutos


def run_once():
    collectors = [
        MockAdsCollector(),
        GoogleAdsCollector(),
        TikTokCreativeCenterCollector()
    ]

    niche_classifier = NicheClassifier()
    language_detector = LanguageDetector()
    score_engine = ScoreEngine()

    all_ads = []
    filtered_ads = []

    for collector in collectors:
        ads = collector.collect()
        all_ads.extend(ads)

    for ad in all_ads:
        headline = ad.get("headline", "")

        niche = niche_classifier.classify(headline)
        detected_language = language_detector.detect_language(headline)

        ad["niche"] = niche
        ad["detected_language"] = detected_language

        score_data = score_engine.calculate_score(ad)

        ad["score"] = score_data["score"]
        ad["status"] = score_data["status"]
        ad["reasons"] = score_data["reasons"]

        active_ads_count = ad.get("active_ads_count", 0)

        is_igaming_priority = (
            ad["niche"] == "igaming" and ad["status"] in ["forte", "escalada"]
        )

        is_other_niche_high_volume = (
            ad["niche"] != "igaming" and active_ads_count >= 100
        )

        if is_igaming_priority or is_other_niche_high_volume:
            filtered_ads.append(ad)

    print("\nOfertas filtradas:\n")

    for ad in filtered_ads:
        print(ad)

    print("\nTotal coletado:", len(all_ads))
    print("Total filtrado:", len(filtered_ads))

    report = "🔥 RADAR DE OFERTAS\n\n"

    if not filtered_ads:
        report += "Nenhuma oferta relevante encontrada nesta rodada."
    else:
        for ad in filtered_ads:
            reasons_text = "\n".join([f"- {reason}" for reason in ad.get("reasons", [])])

            line = f"""Nicho: {ad.get("niche")}
País: {ad.get("country")}
Plataforma: {ad.get("platform")}
Idioma: {ad.get("detected_language")}
Headline: {ad.get("headline")}
Anúncios ativos: {ad.get("active_ads_count")}
Score: {ad.get("score")}
Status: {ad.get("status")}
Landing: {ad.get("landing_url")}
Motivos:
{reasons_text}

--------------------

"""
            report += line

    print("\nRelatório Telegram:\n")
    print(report)

    send_telegram_message(report)


def main():
    print("Radar iniciado em loop de 30 minutos.")

    while True:
        try:
            run_once()
        except Exception as e:
            error_message = f"Erro no radar: {e}"
            print(error_message)
            try:
                send_telegram_message(error_message)
            except Exception as telegram_error:
                print("Erro ao enviar erro para Telegram:", telegram_error)

        print(f"Aguardando {INTERVAL_SECONDS} segundos para próxima rodada...")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

