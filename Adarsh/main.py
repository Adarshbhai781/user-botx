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
    NOT_VIP = "❌ You are not authorized to use this command."
    OWNER_PROTECTED = "❌ You cannot remove the owner!"

OWNER_ID = 7190948267  # Replace with the actual owner ID
VIP_USERS = [OWNER_ID, 987654321]  # Add other VIP user IDs as needed
x = set(VIP_USERS)

# Decorator to restrict commands to the owner and VIP users
def VIP():
    async def decorator(_, __, m: Message):
        if m.from_user.id not in VIP_USERS:
            await m.reply_text(Data.NOT_VIP)
            return False
        return True
    return filters.create(decorator)

@bot.on_message(filters.command("start") & VIP())
async def start(bot, m: Message):
    await m.reply_text(Data.START.format(m.from_user.mention))

@bot.on_message(filters.command("ping") & VIP())
async def ping_pong(bot, m: Message):
    start = asyncio.get_running_loop().time()
    response = await m.reply_text("🏓 Pinging...")
    end = asyncio.get_running_loop().time()
    ping_time = round((end - start) * 1000, 2)
    await response.edit_text(Data.PING.format(ping_time))

@bot.on_message(filters.command("AddSudo", prefixes=["/", "."]) & VIP() & filters.reply)
async def addsudo_list(bot, m: Message):
    if not m.reply_to_message:
        await m.reply_text("❌ Please reply to a user to add them as a VIP.")
        return
    xuser = m.reply_to_message.from_user.id
    x.add(xuser)
    await m.reply_text(Data.VIP_ADDED.format(m.reply_to_message.from_user.mention))

@bot.on_message(filters.command("delsudo", prefixes=["/", "."]) & VIP() & filters.reply)
async def remove_vip(bot, m: Message):
    if not m.reply_to_message:
        await m.reply_text("❌ Please reply to a user to remove them from VIP.")
        return
    xuser = m.reply_to_message.from_user.id
    if xuser == OWNER_ID:
        await m.reply_text(Data.OWNER_PROTECTED)
        return
    if xuser in x:
        x.remove(xuser)
        await m.reply_text(Data.VIP_REMOVED.format(m.reply_to_message.from_user.mention))
    else:
        await m.reply_text("User is not in VIP list.")

@bot.on_message(filters.command("vip") & VIP())
async def vip_handler(bot, m: Message):
    vip_mentions = []
    for user_id in x:
        try:
            user = await bot.get_users(user_id)
            vip_mentions.append(user.mention)
        except Exception:
            vip_mentions.append(f"`{user_id}`")
    vip_list = "\n".join(vip_mentions) or "No VIP users found."
    await m.reply_text(vip_list)

@bot.on_message(filters.command("vipx") & VIP())
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

@bot.on_message(filters.command("stop") & VIP())
async def stop_handler(bot, m: Message):
    await m.reply_text("🚦**STOPPED**🚦")
    os.execl(sys.executable, sys.executable, *sys.argv)

bot.run()
