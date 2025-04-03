import os
import json
import openai
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from sheets_helper import find_patient
from openai_helper import generate_response
from flask import Flask, request

nest_asyncio.apply()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{os.environ.get('RENDER_EXTERNAL_URL', 'https://kine-bot.onrender.com')}{WEBHOOK_PATH}"

app = Flask(__name__)
application = None  # Telegram application instance

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bonjour, je suis votre assistant kiné personnel. Posez-moi vos questions !")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    chat_id = update.message.chat_id
    print(f"📩 [{chat_id}] Message reçu : {user_input}")

    patient = find_patient(user_input)
    if patient:
        contexte = (
            f"Prénom : {patient['prenom']}\n"
            f"Date de naissance : {patient['date_naissance']}\n"
            f"Téléphone : {patient['telephone']}\n"
            f"Antécédents : {patient['antecedents']}\n"
            f"Exercice du jour : {patient['exercice_du_jour']}\n"
            f"Remarques : {patient['remarques']}"
        )
        response = generate_response(contexte, user_input)
    else:
        response = "Je ne vous ai pas trouvé dans la base. Veuillez vérifier votre prénom ou contactez votre kiné."

    await update.message.reply_text(response)

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if application:
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put_nowait(update)
    return "ok"

async def main():
    global application
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.bot.set_webhook(WEBHOOK_URL)
    print("✅ Bot démarré en mode Webhook.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))