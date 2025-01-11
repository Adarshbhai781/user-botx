import os
from pyrogram import Client as Bot, filters
from pyrogram.types import Message
from config import Config

bot = Bot(
    name="Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)

@bot.on_message(filters.command(["op"]))
async def downloader(client: Bot, message: Message):
    target_content = message.reply_to_message
    if not target_content:
        await message.reply_text("Reply to a message containing media to download.")
        return
    download_target_content = await client.download_media(target_content)
    await client.send_document("me", download_target_content)
    os.remove(download_target_content)

bot.run()

