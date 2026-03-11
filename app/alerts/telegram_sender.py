import requests

BOT_TOKEN = "8222014861:AAFQZGVGkZCG6yqeXiQAzbvwGO0cXG-6qtg"
CHAT_ID = "8446101926"


def send_telegram_message(message: str):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)

        if response.status_code == 200:
            print("Mensagem enviada para Telegram.")
        else:
            print("Erro ao enviar:", response.text)

    except Exception as e:
        print("Erro:", e)

