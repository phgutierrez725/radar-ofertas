import time

from app.collectors.google_ads_collector import GoogleAdsCollector
from app.collectors.tiktok_creative_center_collector import TikTokCreativeCenterCollector
from app.collectors.facebook_ads_library_collector import FacebookAdsLibraryCollector
from app.collectors.youtube_ads_collector import YouTubeAdsCollector
from app.collectors.taboola_ads_collector import TaboolaAdsCollector
from app.collectors.outbrain_ads_collector import OutbrainAdsCollector
from app.collectors.kwai_ads_collector import KwaiAdsCollector

from app.classifiers.niche import NicheClassifier
from app.classifiers.language import LanguageDetector

from app.scoring.engine import ScoreEngine
from app.alerts.telegram_sender import send_telegram_message

from app.detectors.new_landing_detector import NewLandingDetector
from app.detectors.new_creative_detector import NewCreativeDetector


INTERVAL_SECONDS = 1800


def run_once():

    collectors = [
        GoogleAdsCollector(),
        TikTokCreativeCenterCollector(),
        FacebookAdsLibraryCollector(),
        YouTubeAdsCollector(),
        TaboolaAdsCollector(),
        OutbrainAdsCollector(),
        KwaiAdsCollector()
    ]

    niche_classifier = NicheClassifier()
    language_detector = LanguageDetector()
    score_engine = ScoreEngine()

    landing_detector = NewLandingDetector()
    creative_detector = NewCreativeDetector()

    all_ads = []
    filtered_ads = []

    for collector in collectors:
        ads = collector.collect()
        all_ads.extend(ads)

    for ad in all_ads:

        headline = ad.get("headline", "")

        niche = niche_classifier.classify(headline)
        language = language_detector.detect_language(headline)

        ad["niche"] = niche
        ad["detected_language"] = language

        score_data = score_engine.calculate_score(ad)

        ad["score"] = score_data["score"]
        ad["status"] = score_data["status"]
        ad["reasons"] = score_data["reasons"]

        landing_url = ad.get("landing_url", "")
        creative_url = ad.get("creative_url", "")

        new_landing = False
        new_creative = False

        if landing_url:
            new_landing = landing_detector.check(landing_url)

        if creative_url:
            new_creative = creative_detector.check(creative_url)

        ad["new_landing"] = new_landing
        ad["new_creative"] = new_creative

        active_ads = ad.get("active_ads_count", 0)

        igaming_priority = (
            ad["niche"] == "igaming"
            and ad["status"] in ["forte", "escalada"]
        )

        other_high_volume = (
            ad["niche"] != "igaming"
            and active_ads >= 100
        )

        if igaming_priority or other_high_volume:
            filtered_ads.append(ad)

    print("\nOfertas filtradas:\n")

    for ad in filtered_ads:
        print(ad)

    print("\nTotal coletado:", len(all_ads))
    print("Total filtrado:", len(filtered_ads))

    report = "🔥 RADAR DE OFERTAS\n\n"

    if not filtered_ads:
        report += "Nenhuma oferta relevante encontrada."
    else:

        for ad in filtered_ads:

            reasons_text = "\n".join(
                [f"- {reason}" for reason in ad.get("reasons", [])]
            )

            message = f"""
Nicho: {ad.get("niche")}
País: {ad.get("country")}
Plataforma: {ad.get("platform")}
Idioma: {ad.get("detected_language")}

Headline:
{ad.get("headline")}

Anúncios ativos: {ad.get("active_ads_count")}
Score: {ad.get("score")}
Status: {ad.get("status")}

Landing:
{ad.get("landing_url")}

Nova landing: {ad.get("new_landing")}
Novo criativo: {ad.get("new_creative")}

Motivos:
{reasons_text}

---------------------
"""

            report += message

    print("\nRelatório Telegram:\n")
    print(report)

    send_telegram_message(report)


def main():

    print("Radar iniciado — scan a cada 30 minutos.")

    while True:

        try:
            run_once()

        except Exception as e:

            error_message = f"Erro no radar: {e}"

            print(error_message)

            try:
                send_telegram_message(error_message)
            except:
                pass

        print(f"Aguardando {INTERVAL_SECONDS} segundos...")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
