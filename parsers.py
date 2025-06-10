import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def parse_ozon(url):
    return {
        "title": "Трусы-боксёры (Ozon)",
        "price": "Цена: 499 ₽",
        "discount": "Скидка: 30%",
        "image": "https://ir.ozone.ru/some_image.jpg",
        "link": url
    }

def parse_wildberries(url):
    return {
        "title": "Паста для чистки (WB)",
        "price": "Цена: 299 ₽",
        "discount": "Скидка: 15%",
        "image": "https://images.wbstatic.net/some_image.jpg",
        "link": url
    }

def parse_yandex_market(url):
    return {
        "title": "Массажер антицеллюлитный (Яндекс.Маркет)",
        "price": "Цена: 999 ₽",
        "discount": "Скидка: 10%",
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
            "price": "",
            "discount": "",
            "image": None,
            "link": url
        }
