import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from parsers import parse_link
import aiohttp

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 10000))


async def is_valid_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content_type = resp.headers.get("Content-Type", "")
                return content_type.startswith("image/")
    except:
        return False


@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.answer("Пришли ссылку на товар — я подготовлю красивый пост!")


@dp.message_handler()
async def handle_link(msg: types.Message):
    url = msg.text.strip()
    data = parse_link(url)

    old_price = data.get("old_price")
    new_price = data.get("price", "—")
    rating = data.get("rating", "—")
    market = data.get("market", "—")
    link = data.get("link")

    price_line = f"<b>{new_price}</b>"
    if old_price and old_price != new_price:
        price_line += f" <s>{old_price}</s>"

    text = f"""
🔹 <b>{data.get("title", "Название неизвестно")}</b>

🛒 Маркетплейс: {market}  
💰 Цена: {price_line}  
🧾 Отзывы: {rating}

🔗 <a href="{link}">Перейти к товару</a>

📌 Полезно? Жми ❤️ и делись с друзьями!
""".strip()

    if data.get("image") and await is_valid_image(data["image"]):
        await bot.send_photo(msg.chat.id, data["image"], caption=text, parse_mode="HTML")
    else:
        await msg.answer(text, parse_mode="HTML")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
