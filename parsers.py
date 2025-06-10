import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_ozon(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Товар с Ozon"

        return {
            "title": title,
            "utp": "Подходит для повседневного использования. Отличный выбор!",
            "market": "Ozon",
            "price": "от 499 ₽",
            "discount": "-30% до 15 июня",
            "delivery": "1–3 дня, доставка из РФ",
            "rating": "★★★★☆ (4.6 / 5)",
            "image": "https://ir.ozone.ru/some_image.jpg",
            "link": url
        }
    except Exception as e:
        print(f"[OZON ERROR] {e}")
        return fallback(url, "Ozon")

def parse_wildberries(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Товар с Wildberries"

        return {
            "title": title,
            "utp": "Практичный товар на каждый день. Берут повторно!",
            "market": "Wildberries",
            "price": "от 299 ₽",
            "discount": "-15% по акции до 12 июня",
            "delivery": "Быстрая доставка из РФ",
            "rating": "★★★★☆ (4.7 / 5)",
            "image": "https://images.wbstatic.net/some_image.jpg",
            "link": url
        }
    except Exception as e:
        print(f"[WB ERROR] {e}")
        return fallback(url, "Wildberries")

def parse_yandex_market(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Товар с Яндекс.Маркета"

        return {
            "title": title,
            "utp": "Популярно на Яндекс.Маркете. Часто заказывают!",
            "market": "Яндекс.Маркет",
            "price": "от 999 ₽",
            "discount": "-10% с купоном до 20 июня",
            "delivery": "Склад в РФ, доставка 2–4 дня",
            "rating": "★★★★☆ (4.5 / 5)",
            "image": "https://avatars.mds.yandex.net/some_image.jpg",
            "link": url
        }
    except Exception as e:
        print(f"[YANDEX ERROR] {e}")
        return fallback(url, "Яндекс.Маркет")

def fallback(url, market):
    return {
        "title": f"Товар с {market}",
        "utp": "Интересный товар — посмотри сам!",
        "market": market,
        "price": "—",
        "discount": "—",
        "delivery": "—",
        "rating": "—",
        "image": None,
        "link": url
    }

def parse_link(url):
    if "ozon.ru" in url:
        return parse_ozon(url)
    elif "wildberries.ru" in url:
        return parse_wildberries(url)
    elif "market.yandex" in url:
        return parse_yandex_market(url)
    else:
        return fallback(url, "Неизвестный маркетплейс")
