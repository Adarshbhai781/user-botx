import os
import sys
import asyncio
import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

bot = Client(
    name="Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
)

@bot.on_message(filters.command("start"))
async def start(bot: Client, m: Message):
    await m.reply_text(f"🌟 Welcome Mere Bhai {m.from_user.mention} 🌟")

@bot.on_message(filters.command(["ping"], prefixes=["/", ".", "!"]))
async def ping(bot: Client, message: Message):
    start = datetime.datetime.now()
    loda = await message.reply_text("**» Gᴇɴɪᴜs**")
    end = datetime.datetime.now()
    mp = (end - start).microseconds / 1000
    await loda.edit_text(f"**🤖 Poɴɢ\n»** `{mp} ms`")
    
OWNER_ID = Config.VIP_USER
VIP_USERS = [OWNER_ID, 7516012736]
x = set(VIP_USERS)

@bot.on_message(filters.command("AddSudo", prefixes=["/", "."]))
async def addsudo_list(bot: Client, m: Message):
    if m.from_user.id not in VIP_USERS:  
        return
    if m.reply_to_message:
        userid = m.reply_to_message.from_user.id  
        name = m.reply_to_message.from_user.mention  
    else:
        args = m.text.split()
        if len(args) < 2:
            await m.reply_text("⚠️ Kripya command ke baad valid user ID de.")
            return
        try:
            userid = int(args[1])  
            name = f"<a href='tg://user?id={userid}'>User</a>"
        except ValueError:
            await m.reply_text("⚠️ Invalid user ID. Kripya valid numeric ID de.")
            return
    x.add(userid)
    await m.reply_text(f"✅ **{name} ko VIP users mein add kar diya gaya hai.**")
    
@bot.on_message(filters.command("dlr", prefixes=["/", "."]))
async def remove_sudo(bot: Client, m: Message):
    if m.from_user.id not in VIP_USERS:  
        return   
    if m.reply_to_message:
        userid = m.reply_to_message.from_user.id  
        name = m.reply_to_message.from_user.mention  
    else:
        args = m.text.split()
        if len(args) < 2:
            await m.reply_text("⚠️ Kripya command ke baad valid user ID de.")
            return
        try:
            userid = int(args[1])  
            name = f"<a href='tg://user?id={userid}'>User</a>"
        except ValueError:
            await m.reply_text("⚠️ Invalid user ID. Kripya valid numeric ID de.")
            return
    x.remove(userid)
    await m.reply_text(f"❌ {name} has been removed from VIP users.")
    
@bot.on_message(filters.command("vip"))
async def vip_handler(bot: Client, m: Message):
    vip_mentions = []
    for user_id in x:
        try:
            user = await bot.get_users(user_id)
            vip_mentions.append(user.mention)
        except Exception:
            vip_mentions.append(f"`{user_id}`")
    vip_list = "\n".join(vip_mentions) or "No VIP users found."
    await m.reply_text(vip_list)
    
    
bot.run()
