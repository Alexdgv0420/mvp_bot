
from aiogram import Bot, Dispatcher, types, executor
from config import TELEGRAM_BOT_TOKEN
from parsers import parse_link

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def start_cmd(msg: types.Message):
    await msg.answer("Привет! Отправь ссылку на товар с Ozon, Wildberries или Яндекс.Маркета, и я подготовлю пост!")

@dp.message_handler()
async def handle_link(msg: types.Message):
    url = msg.text.strip()
    data = parse_link(url)
    text = f"<b>{data['title']}</b>\n<a href='{data['link']}'>Перейти к товару</a>"
    if data["image"]:
        await bot.send_photo(msg.chat.id, data["image"], caption=text, parse_mode="HTML")
    else:
        await msg.answer(text, parse_mode="HTML")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
