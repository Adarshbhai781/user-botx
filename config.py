import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7084278704:AAGA4Pxv05_uTvT_iuCQqn9u4xCkLD9Mzxc")
    API_ID = int(os.environ.get("API_ID", 12380656))
    API_HASH = os.environ.get("API_HASH", "d927c13beaaf5110f25c505b7c071273")
    VIP_USER = os.environ.get("AUTH_USERS", "7190948267").split(',')
