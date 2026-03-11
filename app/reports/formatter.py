def format_ad_message(ad: dict) -> str:
    platform = ad.get("platform", "unknown")
    country = ad.get("country", "unknown")
    language = ad.get("detected_language", "unknown")
    headline = ad.get("headline", "Sem headline")
    active_ads_count = ad.get("active_ads_count", 0)
    score = ad.get("score", 0)
    status = ad.get("status", "unknown")
    landing_url = ad.get("landing_url", "Sem link")
    reasons = ad.get("reasons", [])

    reasons_text = "\n".join([f"- {reason}" for reason in reasons])

    return f"""🔥 OFERTA {status.upper()}

Plataforma: {platform}
País: {country}
Idioma: {language}
Headline: {headline}
Anúncios ativos: {active_ads_count}
Score: {score}
Status: {status}

Motivos:
{reasons_text}

Landing:
{landing_url}
"""
