import requests
from pyrogram import Client as Bot, filters
from config import Config

bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)
@bot.on_message(filters.command(["op"]))
async def downloader(_, message: Message):
    targetcontent = message.reply_to_message
    downloadtargetcontent = await client.download_media(targetcontent)
    send = await client.send_document("me", downloadtargetcontent)
    os.remove(downloadtargetcontent)