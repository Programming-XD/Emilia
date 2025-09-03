import os
from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bson.objectid import ObjectId

from Emilia import custom_filter, BOT_NAME, TOKEN, SUPPORT_CHAT, UPDATE_CHANNEL, START_PIC
from Emilia.anime.bot import get_anime, get_recommendations, auth_link_cmd, logout_cmd, get_additional_info, code_cmd
from Emilia.pyro.connection.connect import connectRedirect
from Emilia.pyro.greetings.captcha.button_captcha import buttonCaptchaRedirect
from Emilia.pyro.greetings.captcha.text_captcha import textCaptchaRedirect
from Emilia.pyro.notes.private_notes import note_redirect
from Emilia.pyro.rules.rules import rulesRedirect
from Emilia.utils.decorators import *
from Emilia.tele.clone import startpic
from Emilia.utils.helper import AUTH_USERS, get_btns
from Emilia.anime.bot import help_

START_TEXT = """
👋 ʜᴇʏ  
ɪ ᴀᴍ [ {} ^_^ ]({})  
🩸 ɪ ᴀᴍ ᴍᴀᴅᴇ ᴡɪᴛʜ ꜱʜɪɴᴏʙɪ ʙʟᴏᴏᴅ  
🛡️ ɪ ᴀᴍ ʜᴇʀᴇ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴀʟʟ ɢʀᴏᴜᴘ ᴡᴏʀᴋꜱ  

✨ Use the buttons below or type /help to explore more!
"""


@Client.on_message(custom_filter.command(commands="start"))
@leavemute
@rate_limit(40, 60)
async def starttt(client, message):
    if len(message.text.split()) == 1:
        if message.chat.type == ChatType.PRIVATE:
            start_pic_url = START_PIC

            buttons = [
                [InlineKeyboardButton("✨ 𝗛𝗲𝗹𝗽", callback_data="help_back")],
                [
                    InlineKeyboardButton("💬 𝗙.𝗢.𝗦 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url=f"https://t.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton("📰 𝗙.𝗢.𝗦 𝗡𝗲𝘄𝘀", url=f"https://t.me/{UPDATE_CHANNEL}"),
                ],
                [InlineKeyboardButton("⚔️ 𝗙.𝗢.𝗦", url="https://t.me/FOREST_OF_SAVIOUR_BOT")], 
            ]

            await message.reply_text(
                START_TEXT.format(BOT_NAME, start_pic_url),
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=False,
            )

        elif message.chat.type != ChatType.PRIVATE:
            await message.reply("👋 ʜᴇʏ\nɪ ᴀᴍ [ {} ^_^ ]({}) \n🩸 ɪ ᴀᴍ ᴍᴀᴅᴇ ᴡɪᴛʜ ꜱʜɪɴᴏʙɪ ʙʟᴏᴏᴅ\n🛡️ ɪ ᴀᴍ ʜᴇʀᴇ ᴛᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴀʟʟ ɢʀᴏᴜᴘ ᴡᴏʀᴋꜱ")

    if len(message.text.split()) > 1:
        user = message.from_user.id
        chat = message.chat.id
        deep_cmd_list = (message.text.split()[1]).split("_")

        # Captcha Redirect Implementation
        if startCheckQuery(message, StartQuery="captcha"):
            await buttonCaptchaRedirect(message)
            await textCaptchaRedirect(message)

        # Private Notes Redirect Implementation
        elif startCheckQuery(message, StartQuery="note"):
            await note_redirect(message)

        # Connection Redirect Implementation
        elif startCheckQuery(message, StartQuery="connect"):
            await connectRedirect(message)

        # Rules Redirect Implementation
        elif startCheckQuery(message, StartQuery="rules"):
            await rulesRedirect(message)

        elif startCheckQuery(message, StartQuery="anihelp"):
            await help_(client, message)

        elif startCheckQuery(message, StartQuery="auth"):
            await auth_link_cmd(client, message)

        elif startCheckQuery(message, StartQuery="logout"):
            await logout_cmd(client, message)

        elif deep_cmd_list[0] == "des":
            try:
                req = deep_cmd_list[3]
            except IndexError:
                req = "desc"
            pic, result = await get_additional_info(
                deep_cmd_list[2], deep_cmd_list[1], req
            )
            await client.send_photo(chat, pic)
            try:
                await client.send_message(
                    chat, result.replace("~!", "").replace("!~", "")
                )
            except (TypeError, AttributeError):
                await client.send_message(chat, "No description available!!!")

        elif deep_cmd_list[0] == "anime":
            auth = False
            if await AUTH_USERS.find_one({"id": user}):
                auth = True
            result = await get_anime(
                {"id": int(deep_cmd_list[1])}, user=user, auth=auth
            )
            pic, msg = result[0], result[1]
            buttons = get_btns("ANIME", result=result, user=user, auth=auth)
            await client.send_photo(chat, pic, caption=msg, reply_markup=buttons)

        elif deep_cmd_list[0] == "anirec":
            result = await get_recommendations(deep_cmd_list[1])
            await client.send_message(user, result, disable_web_page_preview=True)

        elif (message.text.split()[1]).split("_", 1)[0] == "code":
            if not os.environ.get("ANILIST_REDIRECT_URL"):
                return
            qry = (message.text.split()[1]).split("_", 1)[1]
            k = await AUTH_USERS.find_one({"_id": ObjectId(qry)})
            await code_cmd(k["code"], message)


def startCheckQuery(message, StartQuery=None) -> bool:
    if (
        StartQuery in message.text.split()[1].split("_")[0]
        and message.text.split()[1].split("_")[0] == StartQuery
    ):
        return True
    else:
        return False

button = [[InlineKeyboardButton("Clone Commands", callback_data="bot_clone")]]

@Client.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "clone_help":  
        await callback_query.message.reply_text(clone_help, reply_markup=InlineKeyboardMarkup(button))
        await callback_query.message.delete()
        return
    if callback_query.data == "bot_clone":   
        await callback_query.message.reply_text(help_text, disable_web_page_preview=True)
        await callback_query.message.delete()
        return


