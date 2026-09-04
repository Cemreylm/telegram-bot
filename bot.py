if name == "main": app = ApplicationBuilder().token(TOKEN).build() app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)) print("Bot çalışıyor...") app.run_polling()
