import os
import sys
import asyncio
from pyrogram import Client as Bot, filters
from pyrogram.types import Message
from config import Config
from config import *

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
    VIP_REMOVED = "❌ **{0} has been removed from VIP users.**"

x = set(Config.VIP_USERS)  

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

@bot.on_message(filters.command("AddSudo", prefixes=["/", "."]) & filters.reply)
async def addsudo_list(client, message):
    if message.from_user.id in Config.VIP_USER:
        xuser = message.reply_to_message.from_user.id
        x.add(xuser)  
        message.reply_text(f"User {xuser} has been added to sudo users.")
        
@bot.on_message(filters.command("delsudo", prefixes=["/", "."]) & filters.reply)
async def remove_vip(client, message):
    if message.from_user.id in Config.VIP_USERS:
        xuser = message.reply_to_message.from_user.id
        if xuser in x:
            x.remove(xuser) 
            message.reply_text(f"User {xuser} has been removed from VIP users.")
        else:
            message.reply_text(f"User {xuser} is not in the VIP list.")

@bot.on_message(filters.command("vip"))
async def vip_handler(bot, m: Message):
    if m.from_user.id in Config.VIP_USERS:
        reply = m.reply_to_message
        if len(m.command) == 1 and not reply:
            vip_mentions = []
            for user_id in x:
                try:
                    user = await bot.get_users(user_id)
                    vip_mentions.append(user.mention)
                except Exception:
                    vip_mentions.append(f"`{user_id}`")
            vip_list = "\n".join(vip_mentions) or "No VIP users found."
            await m.reply_text(vip_list)


@bot.on_message(filters.command("stop"))
async def restart_handler(bot, m: Message):
    if m.chat.id not in Config.VIP_USERS:
        await bot.send_message(
            m.chat.id,
            f"Oopss! You are not a Team member.",
        )
        return
    await m.reply_text("🚦**STOPPED**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

bot.run()
