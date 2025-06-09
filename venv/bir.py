import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import logging

API_TOKEN = "7767976956:AAHLmuA8vA-sQ8HRdLkOVSFUxAXjcNT4S0A"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_data = {}

def generate_kitobcha_pages(n):
    if n <= 0:
        return [], []

    total = n
    while total % 4 != 0:
        total += 1

    old_tomon = []
    orqa_tomon = []

    left = 1
    right = total

    while left <= total // 2:
        old_tomon.append(right)
        old_tomon.append(left)
        right -= 1
        left += 1

        orqa_tomon.append(left)
        orqa_tomon.append(right)
        left += 1
        right -= 1
    return old_tomon[:n], orqa_tomon[:n]

def generate_majmua_pages(n):
    if n <= 0:
        return [], []

    old_tomon = []
    orqa_tomon = []

    if n % 2 == 0:
        old_tomon = list(range(1, n, 2))
        orqa_tomon = list(range(n, 0, -2))
    else:
        old_tomon = list(range(1, n + 1, 2))
        orqa_tomon = list(range(n - 1, 0, -2))

    return old_tomon, orqa_tomon

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="📖 Kitobcha"),
        types.KeyboardButton(text="📄 Majmua")
    )
    keyboard = builder.as_markup(resize_keyboard=True)
    await message.answer("Turini tanlang:", reply_markup=keyboard)

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text in ["📖 Kitobcha", "📄 Majmua"]:
        user_data[user_id] = {"mode": text}
        await message.answer("Nechta sahifa chop etasiz? Raqam kiriting (masalan, 15):")
        return

    if text.isdigit():
        if user_id not in user_data or "mode" not in user_data[user_id]:
            await message.answer("Iltimos, avval /start buyrug‘ini yuboring.")
            return

        mode = user_data[user_id]["mode"]
        count = int(text)

        if mode == "📖 Kitobcha":
            old, orqa = generate_kitobcha_pages(count)
            total_pages = count
            while total_pages % 4 != 0:
                total_pages += 1
            await message.answer(
                f"📖 *Kitobcha rejimi* 📖\n\n"
                f"🖨️ Jami sahifalar: {total_pages}\n\n"
                f"✅ Varaqning oldi tomoniga chop etiladigan sahifalar raqamlari:\n`{','.join(map(str, old))}`\n\n"
                f"📄 Varaqning orqa tomoniga chop etiladigan sahifalar raqamlari:\n`{','.join(map(str, orqa))}`",
                parse_mode="Markdown"
            )
        elif mode == "📄 Majmua":
            old, orqa = generate_majmua_pages(count)
            await message.answer(
                f"📄 *Majmua rejimi* 📄\n\n"
                f"🖨️ Jami sahifalar: {count}\n\n"
                f"✅ Varaqning oldi tomoniga chop etiladigan sahifalar raqamlari:\n`{','.join(map(str, old))}`\n\n"
                f"📄 Varaqning orqa tomoniga chop etiladigan sahifalar raqamlari:\n`{','.join(map(str, orqa))}`",
                parse_mode="Markdown"
            )
    else:
        await message.answer("Faqat raqam kiriting.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())