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
from app.detectors.new_offer_detector import NewOfferDetector
from app.detectors.escalation_detector import EscalationDetector
from app.detectors.suspicious_domain_detector import SuspiciousDomainDetector
from app.detectors.offer_signal_detector import OfferSignalDetector


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
    offer_detector = NewOfferDetector()
    escalation_detector = EscalationDetector()
    suspicious_domain_detector = SuspiciousDomainDetector()
    offer_signal_detector = OfferSignalDetector()

    all_ads = []
    filtered_ads = []

    blocked_domains = [
        "facebook.com",
        "google.com",
        "youtube.com",
        "tiktok.com",
        "outbrain.com",
        "taboola.com",
        "ads.kwai.com",
        "ads.tiktok.com",
        "adstransparency.google.com"
    ]

    for collector in collectors:
        ads = collector.collect()
        all_ads.extend(ads)

    for ad in all_ads:

        headline = ad.get("headline", "")
        landing_url = ad.get("landing_url", "")
        creative_url = ad.get("creative_url", landing_url)
        active_ads_count = ad.get("active_ads_count", 0)

        skip = False

        for domain in blocked_domains:
            if landing_url and domain in landing_url:
                skip = True
                break

        if skip:
            continue

        niche = niche_classifier.classify(headline)
        detected_language = language_detector.detect_language(headline)

        ad["niche"] = niche
        ad["detected_language"] = detected_language

        score_data = score_engine.calculate_score(ad)

        ad["score"] = score_data["score"]
        ad["status"] = score_data["status"]
        ad["reasons"] = score_data["reasons"]

        ad_id = ad.get("id", landing_url or headline)

        is_new_landing = False
        is_new_creative = False
        is_new_offer = False
        is_escalating = False
        is_suspicious_domain = False
        is_offer_signal = False

        if landing_url:
            is_new_landing = landing_detector.check(landing_url)
            is_new_offer = offer_detector.check(landing_url)
            is_suspicious_domain = suspicious_domain_detector.check(landing_url)

        if creative_url:
            is_new_creative = creative_detector.check(creative_url)

        if ad_id:
            is_escalating = escalation_detector.check(ad_id, active_ads_count)

        is_offer_signal = offer_signal_detector.check(headline)

        ad["new_landing"] = is_new_landing
        ad["new_creative"] = is_new_creative
        ad["new_offer"] = is_new_offer
        ad["escalating"] = is_escalating
        ad["suspicious_domain"] = is_suspicious_domain
        ad["offer_signal"] = is_offer_signal

        should_alert = (
            (is_suspicious_domain and is_escalating)
            or
            (is_offer_signal and is_escalating)
        )

        if should_alert:
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
🚨 OFERTA ESCALANDO

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

Domínio suspeito: {ad.get("suspicious_domain")}
Sinal de oferta: {ad.get("offer_signal")}
Nova oferta: {ad.get("new_offer")}
Nova landing: {ad.get("new_landing")}
Novo criativo: {ad.get("new_creative")}
Escalando: {ad.get("escalating")}

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
