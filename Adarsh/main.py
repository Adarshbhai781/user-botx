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
    PING = "🏓 Pong! Bot is alive.\n⏱ Response Time: `{0}ms`"
    VIP_ADDED = "✅ **{0} has been added to VIP users.**"
    VIP_REMOVED = "✅ **{0} has been removed from VIP users.**"
    VIP_LIST = "🌟 **VIP Users:**\n\n{0}"


VIP_USERS = set(Config.VIP_USERS)


@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user = await bot.get_me()
    mention = user.mention
    start_message = await bot.send_message(
        m.chat.id, Data.START.format(m.from_user.mention)
    )

    progress_texts = [
        "Initializing Your bot... 🤖\n\nProgress: [⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 0%\n\n",
        "Loading features... ⏳\n\nProgress: [🟥🟥🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 25%\n\n",
        "This may take a moment, sit back and relax! 😊\n\nProgress: [🟧🟧🟧🟧🟧⬜️⬜️⬜️⬜️⬜️] 50%\n\n",
        "Checking subscription status... 🔍\n\nProgress: [🟨🟨🟨🟨🟨🟨🟨🟨⬜️⬜️] 75%\n\n",
    ]

    for text in progress_texts:
        await asyncio.sleep(1)
        await start_message.edit_text(Data.START.format(m.from_user.mention) + text)

    if m.chat.id in VIP_USERS:
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
@bot.on_message(filters.command("ping"))
async def ping_pong(bot, m: Message):
    start = asyncio.get_event_loop().time()
    response = await m.reply_text("🏓 Pinging...")
    end = asyncio.get_event_loop().time()
    ping_time = round((end - start) * 1000, 2)
    await response.edit_text(Data.PING.format(ping_time))


@bot.on_message(filters.command("vip"))
async def vip_handler(bot, m: Message):
    if len(m.command) < 2:
        vip_mentions = []
        for user_id in VIP_USERS:
            try:
                user = await bot.get_users(user_id)
                vip_mentions.append(user.mention)
            except Exception:
                vip_mentions.append(f"`{user_id}`")
        vip_list = "\n".join(vip_mentions) or "No VIP users found."
        await m.reply_text(Data.VIP_LIST.format(vip_list))
        return

    action = m.command[1].lower()
    if action == "add" and len(m.command) == 3:
        user_id = int(m.command[2])
        VIP_USERS.add(user_id)
        try:
            user = await bot.get_users(user_id)
            mention = user.mention
        except Exception:
            mention = f"`{user_id}`"
        await m.reply_text(Data.VIP_ADDED.format(mention))
    elif action == "remove" and len(m.command) == 3:
        user_id = int(m.command[2])
        if user_id in VIP_USERS:
            VIP_USERS.remove(user_id)
            try:
                user = await bot.get_users(user_id)
                mention = user.mention
            except Exception:
                mention = f"`{user_id}`"
            await m.reply_text(Data.VIP_REMOVED.format(mention))
        else:
            await m.reply_text("❌ User is not in VIP users list.")
    else:
        await m.reply_text("❓ Invalid command format.\nUse `/vip`, `/vip add <user_id>`, or `/vip remove <user_id>`.")


@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m: Message):
    if m.chat.id not in VIP_USERS:
        await bot.send_message(
            m.chat.id,
            f"""**Oopss! You are not a Premium member.**\n\n**PLEASE UPGRADE YOUR PLAN**\n\n**/upgrade for Plan Details**\n**Send me your user ID for authorization. Your User ID is** - `{m.chat.id}`\n\n**NHI MILEGA BABU.**""",
        )
        return
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run()
