import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# Token'lar Render'daki gizli ayarlardan alınacak
TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

# Hugging Face üzerinden ücretsiz sunulan yapay zeka modelinin API adresi
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text

  payload = {
      "inputs": user_message,
      "parameters": {"max_new_tokens": 512, "return_full_text": False},
  }

  try:
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list) and len(result) > 0:
      bot_reply = result[0].get(
          "generated_text", "Yapay zekadan anlamlı bir yanıt alamadım."
      )
    elif isinstance(result, dict) and "error" in result:
      bot_reply = (
          f"Model şu an ısınıyor / yükleniyor, lütfen 1 dakika sonra tekrar"
          f" deneyin: {result['error']}"
      )
    else:
      bot_reply = "Beklenmeyen bir yanıt alındı."
  except Exception as e:
    bot_reply = "Yapay zekaya bağlanırken bir hata oluştu."

  await update.message.reply_text(bot_reply)


if __name__ == "__main__":
  app = ApplicationBuilder().token(TOKEN).build()
  app.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
  )
  print("Yapay zekalı bot çalışıyor...")
  app.run_polling()
