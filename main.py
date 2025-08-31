from fastapi import FastAPI, Request
import asyncio
from bot import create_bot_application, process_update, keep_alive
from contextlib import asynccontextmanager
import os

bot_app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot_app
    bot_app = create_bot_application()
    await bot_app.initialize()
    # await bot_app.start()
    webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL', 'https://redbot-xgi5.onrender.com')}/webhook"
    webhook_info = await bot_app.bot.get_webhook_info()
    if webhook_info.url != webhook_url:
        await bot_app.bot.set_webhook(url=webhook_url)
        print(f"Webhook set to {webhook_url}")
    else:
        print(f"Webhook already set to {webhook_url}")

    # asyncio.create_task(bot_app.updater.start_polling())
    # print("Bot is running...")

    keep_alive()  #to ping render every 10 minutes

    yield

    # await bot_app.stop()
    await bot_app.bot.delete_webhook()
    await bot_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "Telegram bot running with FastAPI"}

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming webhook updates from Telegram"""
    json_data = await request.json()
    await process_update(bot_app, json_data)
    return {"ok": True}

