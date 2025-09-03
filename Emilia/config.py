import json
import os


def get_user_list(config, key):
    with open("{}/Emilia/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    API_HASH = "f4815b9a16cb03c2f5eabe8db1cb0903" # API_HASH from my.telegram.org
    API_ID = 18990697 # API_ID from my.telegram.org

    BOT_ID = 7011123946 # BOT_ID
    BOT_USERNAME = "KakashiHatakeXD_Bot" # BOT_USERNAME

    MONGO_DB_URL = "mongodb+srv://publicDB:publicDBbyKira@public.twckcqf.mongodb.net" # MongoDB URL from MongoDB Atlas

    SUPPORT_CHAT = "FOS_Community" # Support Chat Username
    UPDATE_CHANNEL = "FOREST_OF_SAVIOUR" # Update Channel Username
    START_PIC = "https://pic-bstarstatic.akamaized.net/ugc/9e98b6c8872450f3e8b19e0d0aca02deff02981f.jpg@1200w_630h_1e_1c_1f.webp" # Start Image
    DEV_USERS = [6632519077] # Dev Users
    TOKEN = "7011123946:AAH6OMw44iRmGFBObURfZNcPP8xQEZM1JMw" # Bot Token from @BotFather
    CLONE_LIMIT = 50 # Number of clones your bot can make

    EVENT_LOGS = -10093 # Event Logs Chat ID
    OWNER_ID = 6632519077
 
    TEMP_DOWNLOAD_DIRECTORY = "./" # Temporary Download Directory
    BOT_NAME = "Kakashi" # Bot Name
    WALL_API = "6950f53" # Wall API from wall.alphacoders.com


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
