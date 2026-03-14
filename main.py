import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ==========================================
# ТВОИ ДАННЫЕ
# ==========================================
TELEGRAM_TOKEN = "8669656221:AAHr9dzCxh57AVHNLebN6wzVV4kn03jx7n4"
GROQ_API_KEY = "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"

# Твоя выбранная сверхбыстрая модель
MODEL_ID = "llama-3.1-8b-instant"

# ==========================================
# ОБРАБОТЧИК СООБЩЕНИЙ
# ==========================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Показываем статус "печатает..." в Телеге
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Стандартный адрес Groq API
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "Ты — Морфин, умный и дерзкий ИИ-помощник. Отвечай на русском языке коротко и по делу."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    answer = data["choices"][0]["message"]["content"].strip()
                    await update.message.reply_text(answer)
                else:
                    error_text = await resp.text()
                    await update.message.reply_text(f"❌ Ошибка Groq ({resp.status}):\n{error_text}")
    except Exception as e:
        await update.message.reply_text(f"❌ Системная ошибка сети:\n{e}")

# ==========================================
# ЗАПУСК
# ==========================================
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(">>> Бот запущен через сверхбыстрый Groq с моделью Llama 3.1!")
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
