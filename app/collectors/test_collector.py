import requests
from bs4 import BeautifulSoup

def collect_page(url):
    print(f"Coletando: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao acessar página")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else "Sem título"

    print("Título da página:")
    print(title)


if __name__ == "__main__":
    url = "https://example.com"
    collect_page(url)
