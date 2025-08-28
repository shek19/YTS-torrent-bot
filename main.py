from fastapi import FastAPI
import asyncio
from bot import create_bot_application
from contextlib import asynccontextmanager

bot_app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot_app
    bot_app = create_bot_application()
    await bot_app.initialize()
    await bot_app.start()

    asyncio.create_task(bot_app.updater.start_polling())
    print("Bot is running...")

    yield

    await bot_app.stop()
    await bot_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "Telegram bot running with FastAPI"}


