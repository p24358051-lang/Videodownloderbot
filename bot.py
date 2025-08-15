import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Main ek video provider bot hoon. Mujhe ek video URL ya keyword bhejo.")

def send_video(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_message = update.message.text
    video_url = "https://www.pexels.com/video/9963201/download/"  # Example video URL
    caption = "Yeh aapka video hai!"
    try:
        context.bot.send_video(chat_id=chat_id, video=video_url, caption=caption)
        update.message.reply_text("Video successfully bhej diya gaya!")
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        update.message.reply_text("Video bhejne mein error aaya. Kripaya dobara try karein.")

def main() -> None:
    updater = Updater("7597019774:AAGeR8Gmpszd60TLx2WfZJcop-epyLyq-Qc", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
