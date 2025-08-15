from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters
import logging
import yt_dlp
import os

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("YouTube Video", callback_data='youtube')],
        [InlineKeyboardButton("Sample Video", callback_data='sample')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Ek option chuniye:", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'youtube':
        await query.message.reply_text("Kripaya YouTube URL bhejo!")
    elif query.data == 'sample':
        video_url = "https://cdn.pixabay.com/video/2023/05/15/676548-824696723_large.mp4"
        await context.bot.send_video(chat_id=query.message.chat_id, video=video_url, caption="Sample Video")
        await query.message.reply_text("Sample video bhej diya gaya!")

async def send_video(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_message = update.message.text
    video_url = user_message

    if "youtube.com" in video_url or "youtu.be" in video_url:
        download_dir = '/storage/emulated/0/Download/'
        if not os.path.exists(download_dir):
            await update.message.reply_text("Download directory nahi mil raha. Storage permission check karein.")
            return
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'ffmpeg_location': '/data/data/com.termux/files/usr/bin/ffmpeg',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_path = ydl.prepare_filename(info)
                if not video_path.endswith('.mp4'):
                    video_path = video_path.rsplit('.', 1)[0] + '.mp4'
                file_size = os.path.getsize(video_path)
                max_size = 100 * 1024 * 1024  # 100MB limit (badhaya gaya)
                if file_size > max_size:
                    await update.message.reply_text(f"Video {file_size/(1024*1024):.2f}MB hai, jo {max_size/(1024*1024)}MB se bada hai. Chhota video try karein.")
                    os.remove(video_path)
                    return
                with open(video_path, 'rb') as video_file:
                    await context.bot.send_video(chat_id=chat_id, video=video_file, caption=info['title'])
                await update.message.reply_text("Video successfully bhej diya gaya!")
                os.remove(video_path)  # Cleanup
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Download error: {e}")
            await update.message.reply_text(f"Video download karne mein error aaya: {str(e)}. Kripaya valid URL try karein.")
        except PermissionError as e:
            logger.error(f"Permission error: {e}")
            await update.message.reply_text("Storage permission nahi hai. 'termux-setup-storage' run karein.")
        except OSError as e:
            logger.error(f"OS error: {e}")
            await update.message.reply_text("File access mein problem. Download directory check karein.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await update.message.reply_text(f"Kuch galat ho gaya: {str(e)}. Kripaya dobara try karein.")
    else:
        await update.message.reply_text("Kripaya ek valid YouTube URL bhejo!")

def main() -> None:
    # Application class ka use karke bot initialize karein
    application = Application.builder().token("7597019774:AAGeR8Gmpszd60TLx2WfZJcop-epyLyq-Qc").build()

    # Handlers add karein
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_video))

    # Bot shuru karein
    application.run_polling()

if __name__ == '__main__':
    main()
