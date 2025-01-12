import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    VIP_USER = os.environ.get('AUTH_USERS', '').split(',')
class Data:
    START = "🌟 Welcome Mere Bhai {0}! 🌟\n\n"
    PING = "🏓 Pong! Bot is alive.\n⏱ Response Time: `{0}ms`"
    VIP_ADDED = "✅ **{0} has been added to VIP users.**"
    VIP_REMOVED = "❌ **{0} has been removed from VIP users.**"
    NOT_VIP = "❌ You are not authorized to use this command."
    OWNER_PROTECTED = "❌ You cannot remove the owner!"
    
    