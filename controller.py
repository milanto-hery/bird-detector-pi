from config import TELEGRAM_TOKEN, CHAT_ID
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import subprocess
import os
import signal

DETECTION_SCRIPT = 'bird_classifier.py'
DETECTION_PROCESS = None

def start(update: Update, context: CallbackContext):
    global DETECTION_PROCESS
    if DETECTION_PROCESS is None:
        DETECTION_PROCESS = subprocess.Popen(['python3', DETECTION_SCRIPT])
        update.message.reply_text("🐦 Bird detection started.")
    else:
        update.message.reply_text("⚠️ Detection is already running.")

def stop(update: Update, context: CallbackContext):
    global DETECTION_PROCESS
    if DETECTION_PROCESS is not None:
        os.kill(DETECTION_PROCESS.pid, signal.SIGTERM)
        DETECTION_PROCESS = None
        update.message.reply_text("🛑 Bird detection stopped.")
    else:
        update.message.reply_text("⚠️ No detection is currently running.")

def status(update: Update, context: CallbackContext):
    if DETECTION_PROCESS is not None:
        update.message.reply_text("✅ Bird detection is running.")
    else:
        update.message.reply_text("❌ Bird detection is not running.")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("status", status))

    updater.start_polling()
    print("Telegram bot controller running...")
    updater.idle()

if __name__ == '__main__':
    main()
