import os
from aiogram import Bot, Dispatcher, types, executor
from parsers import parse_link

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def start_cmd(msg: types.Message):
    await msg.answer("Привет! Пришли ссылку на товар с Ozon, Wildberries или Яндекс.Маркета, и я сделаю карточку товара для канала 💬")

@dp.message_handler()
async def handle_link(msg: types.Message):
    url = msg.text.strip()
    data = parse_link(url)

    # Шаблон поста
    post_text = f"""
<b>{data.get("title", "Товар")}</b>

{data.get("price", "")}
{data.get("discount", "")}

<a href="{data.get("link")}">🛒 Открыть товар</a>
""".strip()

    if data.get("image"):
        await bot.send_photo(msg.chat.id, photo=data["image"], caption=post_text, parse_mode="HTML")
    else:
        await msg.answer(post_text, parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
