import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    VIP_USER = os.environ.get('AUTH_USERS', '').split(',')
    VIP_USERS = [int(user_id) for user_id in VIP_USER]
    DB_NAME = "Non_DRM_Bot"
    DB_URL = "mongodb+srv://srikantkumar2025:QC5M1BgTGxxUqM4R@cluster0.u6zhg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    HOST = "https://drm-api-six.vercel.app"
