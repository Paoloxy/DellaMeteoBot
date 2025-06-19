import os
import datetime
import pytz
from dotenv import load_dotenv
from telegram import Update, ChatAction
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext
)

from generate_audio import generate_audio
from generate_script import generate_script
from meteo_settimanale import meteo_settimanale

# === CONFIGURAZIONE ===

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID_TARGET = -1002724567822
italy_tz = pytz.timezone("Europe/Rome")

# === HANDLER /start ===

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id
    print(f"[start] Utente ha avviato il bot - Telegram ID: {user.id}, Chat ID: {chat_id}, Username: @{user.username}")
    update.message.reply_text("✅ Ciao! Usa /try per ricevere il meteo vocale ora. Lo riceverai ogni giorno alle 8!")

# === HANDLER /try ===

def try_now(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    print(f"[try_now] Esecuzione manuale richiesta da Telegram ID: {user_id}, Chat ID: {chat_id}")
    try:
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_VOICE)
        summary = meteo_settimanale()
        script = generate_script(summary, "Trento")
        audio = generate_audio(script)
        context.bot.send_voice(chat_id=chat_id, voice=open(audio, "rb"))
        print(f"[try_now] Audio vocale inviato correttamente all'utente {user_id}.")
    except Exception as e:
        print(f"[try_now] Errore per utente {user_id}: {e}")

# === JOB AUTOMATICO ===

def meteo_periodico(context: CallbackContext):
    print(f"[meteo_periodico] Invio automatico al gruppo {CHAT_ID_TARGET}")
    try:
        context.bot.send_chat_action(chat_id=CHAT_ID_TARGET, action=ChatAction.RECORD_VOICE)
        summary = meteo_settimanale()
        script = generate_script(summary, "Trento")
        audio = generate_audio(script)
        context.bot.send_voice(chat_id=CHAT_ID_TARGET, voice=open(audio, "rb"))
        print("[meteo_periodico] Audio inviato con successo.")
    except Exception as e:
        print(f"[meteo_periodico] Errore: {e}")

# === AVVIO BOT ===

def main():
    print("[main] Avvio bot Telegram...")
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("try", try_now))

    # Pianifica job ogni giovedì alle 19:34 (ora italiana)
    time_it = datetime.time(hour=19, minute=42, tzinfo=italy_tz)
    updater.job_queue.run_daily(meteo_periodico, time=time_it, days=(3,), name="meteo_settimanale")

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
