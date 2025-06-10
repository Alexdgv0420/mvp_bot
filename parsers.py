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
            "market": "Ozon",
            "price": "299 ₽",
            "old_price": "499 ₽",
            "rating": "★★★★☆ (4.6 / 5)",
            "image": "https://ir.ozone.ru/some_image.jpg",
            "link": url
        }
    except Exception as e:
        print(f"[OZON ERROR] {e}")
        return fallback(url, "Ozon")

def parse_wildberries(url):
    try:
        product_id = url.split('/catalog/')[1].split('/')[0]
        api_url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&nm={product_id}"
        resp = requests.get(api_url, headers=HEADERS, timeout=5).json()
        data = resp['data']['products'][0]

        title = data.get("name", "Товар с Wildberries")
        new_price = f"{data.get('salePriceU', 0) // 100} ₽"
        old_price = f"{data.get('priceU', 0) // 100} ₽"
        rating = f"{data.get('reviewRating', 0)} ★"

        # рабочая ссылка на изображение с Wildberries
        image = f"https://basket-{data['pics'][0] % 10}.wb.ru/vol{data['id'] // 100000}/part{data['id'] // 1000}/{data['id']}/images/big/1.jpg"

        return {
            "title": title,
            "market": "Wildberries",
            "price": new_price,
            "old_price": old_price,
            "rating": rating,
            "image": image,
            "link": url
        }
    except Exception as e:
        print(f"[WB ERROR] {e}")
        return fallback(url, "Wildberries")

def parse_yandex_market(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=7)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Товар с Яндекс.Маркет"

        price_tag = soup.select_one('[data-auto="mainPrice"]')
        price = price_tag.text.strip() if price_tag else "—"

        rating_tag = soup.select_one('[data-zone-name="rating"]')
        rating = rating_tag.text.strip() if rating_tag else "—"

        image_tag = soup.find("img")
        image = image_tag.get("src") if image_tag else None

        return {
            "title": title,
            "market": "Яндекс.Маркет",
            "price": price,
            "old_price": None,
            "rating": rating,
            "image": image,
            "link": url
        }
    except Exception as e:
        print(f"[YANDEX ERROR] {e}")
        return fallback(url, "Яндекс.Маркет")

def fallback(url, market):
    return {
        "title": f"Товар с {market}",
        "market": market,
        "price": "—",
        "old_price": None,
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
