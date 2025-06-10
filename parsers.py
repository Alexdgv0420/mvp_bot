import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_ozon(url):
    return {
        "title": "Трусы-боксёры (Ozon)",
        "utp": "Идеально для повседневной носки. 4 штуки в комплекте!",
        "market": "Ozon",
        "price": "от 499 ₽",
        "discount": "-30% до 15 июня",
        "delivery": "1–3 дня, доставка из РФ",
        "rating": "★★★★☆ (4.6 / 5)",
        "image": "https://ir.ozone.ru/some_image.jpg",
        "link": url
    }

def parse_wildberries(url):
    return {
        "title": "Паста для чистки (WB)",
        "utp": "Универсальное средство для кухни, ванной и авто.",
        "market": "Wildberries",
        "price": "от 299 ₽",
        "discount": "-15% по акции до 12 июня",
        "delivery": "Быстрая доставка из РФ",
        "rating": "★★★★☆ (4.7 / 5)",
        "image": "https://images.wbstatic.net/some_image.jpg",
        "link": url
    }

def parse_yandex_market(url):
    return {
        "title": "Массажер антицеллюлитный (Яндекс.Маркет)",
        "utp": "Помогает восстановлению мышц и борется с целлюлитом.",
        "market": "Яндекс.Маркет",
        "price": "от 999 ₽",
        "discount": "-10% с купоном до 20 июня",
        "delivery": "Склад в РФ, доставка 2–4 дня",
        "rating": "★★★★☆ (4.5 / 5)",
        "image": "https://avatars.mds.yandex.net/some_image.jpg",
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
        return {
            "title": "Неизвестный магазин",
            "utp": "Интересный товар — посмотри сам!",
            "market": "—",
            "price": "—",
            "discount": "—",
            "delivery": "—",
            "rating": "—",
            "image": None,
            "link": url
        }
