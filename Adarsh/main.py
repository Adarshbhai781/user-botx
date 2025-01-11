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
 

VIP_USERS = set(Config.VIP_USERS)

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user = await bot.get_me()
    mention = user.mention
    start_message = await bot.send_message(
        m.chat.id, Data.START.format(m.from_user.mention)
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
    reply = m.reply_to_message
    if len(m.command) == 1 and not reply:
        # Show the list of VIP users
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

    if reply:
        user_id = reply.from_user.id
        username = reply.from_user.mention
    elif len(m.command) == 2:
        user_id = int(m.command[1])
        try:
            user = await bot.get_users(user_id)
            username = user.mention
        except Exception:
            username = f"`{user_id}`"
    else:
        await m.reply_text("❓ Invalid command format. Reply to a user or use `/vip <user_id>`.")
        return

    if user_id in VIP_USERS:
        VIP_USERS.remove(user_id)
        await m.reply_text(Data.VIP_REMOVED.format(username))
    else:
        VIP_USERS.add(user_id)
        await m.reply_text(Data.VIP_ADDED.format(username))

@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m: Message):
    if m.chat.id not in VIP_USERS:
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
