from telegram import Update, InputFile
from telegram.ext import Application, ContextTypes, CommandHandler
import aiohttp
import tempfile
import os
from utils.yts_api import search_movies, get_torrent
from config import TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send /movie <movie name> to search for a movie.")


async def download_torrent_file(session: aiohttp.ClientSession, url:str, filename:str):
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://yts.mx/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                temp_dir = tempfile.gettempdir()
                file_path = os.path.join(temp_dir, filename)

                with open(file_path, 'wb') as file:
                    async for chunk in response.content.iter_chunked(8192):
                        file.write(chunk)

                print("Downloaded torrent file : ",filename)
                return file_path
            else:
                print(f"failed to download {url}, status: {response.status}")
                return None
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a movie name after the /movie command. Movie title (you can include year e.g. 'The Thing 1982')")
        return
    
    query = " ".join(context.args)
    progress_msg = await update.message.reply_text("🔍 Searching for movie...")

    movie_id = search_movies(query)
    if not movie_id:
        await progress_msg.edit_text("❌ Movie not found. Please enter the correct movie name.")
        return
    
    await progress_msg.edit_text("📥 Getting torrent information...")
    title, year, torrents = get_torrent(movie_id)

    if not torrents:
        await progress_msg.edit_text("❌ No torrents found for this movie.")
        return

    await progress_msg.edit_text("⬇️ Downloading torrent files...")

    async with aiohttp.ClientSession() as session:
        downloaded_files = []
        
        for i, torrent in enumerate(torrents[:3]):  # Limit to first 3 torrents to avoid spam
            try:
                # Generate filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                filename = f"{safe_title}_{year}_{torrent['quality']}.torrent"
                
                # Download the torrent file
                file_path = await download_torrent_file(session, torrent['url'], filename)
                
                if file_path and os.path.exists(file_path):
                    downloaded_files.append({
                        'path': file_path,
                        'filename': filename,
                        'quality': torrent['quality'],
                        'size': torrent['size']
                    })
                else:
                    print(f"Failed to download torrent: {torrent['quality']}")
                    
            except Exception as e:
                print(f"Error processing torrent {torrent['quality']}: {str(e)}")
                continue
    
    # Delete the progress message
    await progress_msg.delete()
    
    if downloaded_files:
        # Send movie info first
        info_msg = f"🎬 **{title} ({year})**\n\n"
        info_msg += f"📁 Found {len(downloaded_files)} torrent file(s):\n"
        for file_info in downloaded_files:
            info_msg += f"• {file_info['quality']} ({file_info['size']})\n"
        
        await update.message.reply_text(info_msg, parse_mode='Markdown')
        
        # Send each torrent file
        for file_info in downloaded_files:
            try:
                with open(file_info['path'], 'rb') as torrent_file:
                    await update.message.reply_document(
                        document=InputFile(torrent_file, filename=file_info['filename']),
                        caption=f"🎬 {title} ({year}) - {file_info['quality']}\n📦 Size: {file_info['size']}"
                    )
                
                # Clean up the temporary file
                os.remove(file_info['path'])
                
            except Exception as e:
                print(f"Error sending file {file_info['filename']}: {str(e)}")
                await update.message.reply_text(f"❌ Failed to send {file_info['quality']} torrent file.")
                
                # Try to clean up file even if sending failed
                try:
                    if os.path.exists(file_info['path']):
                        os.remove(file_info['path'])
                except:
                    pass
    else:
        await update.message.reply_text("❌ Failed to download any torrent files. The source might be unavailable.")

def create_bot_application():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", movie))

    print("Bot is running...")
    return application

async def process_update(application: Application, update_data: dict):
    """Process incoming webhook update"""
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)