import os
import sys
import asyncio
from pyrogram import Client as Bot, filters
from pyrogram.types import Message
from config import Config

bot = Bot(
    name="Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)


class Data:
    START = "🌟 Welcome Mere Bhai {0}! 🌟\n\n"


@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user = await bot.get_me()
    mention = user.mention
    start_message = await bot.send_message(
        m.chat.id, Data.START.format(m.from_user.mention)
    )

    progress_texts = [
        "Initializing Uploader bot... 🤖\n\nProgress: [⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 0%\n\n",
        "Loading features... ⏳\n\nProgress: [🟥🟥🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 25%\n\n",
        "This may take a moment, sit back and relax! 😊\n\nProgress: [🟧🟧🟧🟧🟧⬜️⬜️⬜️⬜️⬜️] 50%\n\n",
        "Checking subscription status... 🔍\n\nProgress: [🟨🟨🟨🟨🟨🟨🟨🟨⬜️⬜️] 75%\n\n",
    ]

    for text in progress_texts:
        await asyncio.sleep(1)
        await start_message.edit_text(Data.START.format(m.from_user.mention) + text)

    if m.chat.id in Config.VIP_USERS:
        await start_message.edit_text(
            Data.START.format(m.from_user.mention)
            + "`Great! You are a premium member! `🌟\n\n"
            "**If you face any problem, contact us.**"
        )
    else:
        await asyncio.sleep(2)
        await start_message.edit_text(
            Data.START.format(m.from_user.mention)
            + """
✨ **Oops! You are not a premium member.**
"""
        )


@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m: Message):
    if m.chat.id not in Config.VIP_USERS:
        await bot.send_message(
            m.chat.id,
            f"""**Oopss! You are not a Premium member.**\n\n**PLEASE UPGRADE YOUR PLAN**\n\n**/upgrade for Plan Details**\n**Send me your user ID for authorization. Your User ID is** - `{m.chat.id}`\n\n**Sab kuch free me chahiye kya be laude.**""",
        )
        return
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


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
