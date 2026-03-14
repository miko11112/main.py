import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. НАСТРОЙКА GEMINI
# Твой ключ, который ты получил
genai.configure(api_key="AIzaSyDDQ4bVxfooF1c7vmEO-fia0soZ4fzioxM")

# Настраиваем модель (добавляем ей "личность")
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Ты — Gemini, умный и дружелюбный ИИ. Отвечай на русском языке, будь лаконичен и полезен."
)

# 2. НАСТРОЙКА TELEGRAM
# Вставь сюда токен, который дал @BotFather
TELEGRAM_TOKEN = "8669656221:AAHr9dzCxh57AVHNLebN6wzVV4kn03jx7n4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Создаем чат с историей сообщений
chat_session = model.start_chat(history=[])

# Обработка команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет я ии морфина")

# Обработка всех входящих текстовых сообщений
@dp.message()
async def message_handler(message: types.Message):
    # Показываем статус "печатает...", пока нейросеть думает
    await bot.send_chat_action(message.chat.id, action="typing")
    
    try:
        # Отправляем текст в Gemini
        response = chat_session.send_message(message.text)
        
        # Отправляем ответ пользователю (поддерживаем Markdown)
        await message.answer(response.text, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка при обращении к нейросети. Попробуй позже.")

# Запуск бота
async def main():
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Настраиваем логирование, чтобы видеть ошибки в консоли
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")