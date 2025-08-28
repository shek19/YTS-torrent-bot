from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from utils.yts_api import search_movies, get_torrent
from config import TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send /movie <movie name> to search for a movie.")

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a movie name after the /movie command. Movie title (you can include year e.g. 'The Thing 1982')")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text("Searching for movie...")

    movie_id = search_movies(query)
    if not movie_id:
        await update.message.reply_text("Movie not found. Please enter the correct movie name.")
        return
    
    title, year, torrents = get_torrent(movie_id)

    msg = f"🎬 {title} ({year})\n\n"
    for t in torrents:
        msg += f"📥 {t['quality']} | {t['size']}\n{t['url']}\n\n"

    await update.message.reply_text(msg)

def create_bot_application():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", movie))

    print("Bot is running...")
    return application
