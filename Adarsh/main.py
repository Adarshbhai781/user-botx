import os
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

bot = Client(
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

VIP_USERS = []
x = set(VIP_USERS)

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    await m.reply_text(Data.START.format(m.from_user.mention))

@bot.on_message(filters.command("ping"))
async def ping_pong(bot, m: Message):
    start = asyncio.get_event_loop().time()
    response = await m.reply_text("🏓 Pinging...")
    end = asyncio.get_event_loop().time()
    ping_time = round((end - start) * 1000, 2)
    await response.edit_text(Data.PING.format(ping_time))

@bot.on_message(filters.command("AddSudo", prefixes=["/", "."]) & filters.reply)
async def addsudo_list(bot, m: Message):
    xuser = m.reply_to_message.from_user.id
    x.add(xuser)
    await m.reply_text(Data.VIP_ADDED.format(m.reply_to_message.from_user.mention))

@bot.on_message(filters.command("delsudo", prefixes=["/", "."]) & filters.reply)
async def remove_vip(bot, m: Message):
    xuser = m.reply_to_message.from_user.id
    if xuser in x:
        x.remove(xuser)
        await m.reply_text(Data.VIP_REMOVED.format(m.reply_to_message.from_user.mention))
    else:
        await m.reply_text("User is not in VIP list.")

@bot.on_message(filters.command("vip"))
async def vip_handler(bot, m: Message):
    if m.from_user.id in VIP_USERS:
        vip_mentions = []
        for user_id in x:
            try:
                user = await bot.get_users(user_id)
                vip_mentions.append(user.mention)
            except Exception:
                vip_mentions.append(f"`{user_id}`")
        vip_list = "\n".join(vip_mentions) or "No VIP users found."
        await m.reply_text(vip_list)
    else:
        await m.reply_text("You are not authorized to use this command.")

@bot.on_message(filters.command("vipx"))
async def vipx_handler(bot, m: Message):
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
async def stop_handler(bot, m: Message):
    if m.from_user.id not in VIP_USERS:
        await m.reply_text("Oopss! You are not a Team member.")
        return
    await m.reply_text("🚦**STOPPED**🚦")
    os.execl(sys.executable, sys.executable, *sys.argv)

bot.run()
