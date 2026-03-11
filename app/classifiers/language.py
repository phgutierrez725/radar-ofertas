from langdetect import detect


class LanguageDetector:

    def detect_language(self, text: str):

        if not text:
            return "unknown"

        try:
            lang = detect(text)
            return lang
        except:
            return "unknown"
