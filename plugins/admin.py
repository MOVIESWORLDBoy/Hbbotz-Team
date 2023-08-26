import re, asyncio, time, shutil, psutil, os, sys
import datetime
import pytz
from pyrogram import Client, filters, enums
from pyrogram.types import *
from info import BOT_START_TIME, ADMINS
from utils import humanbytes  


@Client.on_message(filters.private & filters.command("status"))          
async def stats(bot, update):
    currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    ms_g = f"""<b><u>𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝘀𝘁𝗮𝘁𝘂𝘀 𝗼𝗳 𝘆𝗼𝘂𝗿 𝗕𝗼𝘁</b></u>

🕔 𝖴𝗉𝗍𝗂𝗆𝖾: <code>{currentTime}</code>
🛠 𝖢𝖯𝖴 𝖴𝗌𝖺𝗀𝖾: <code>{cpu_usage}%</code>
🗜 𝖱𝖠𝖬 𝖴𝗌𝖺𝗀𝖾: <code>{ram_usage}%</code>
🗂 𝖳𝗈𝗍𝖺𝗅 𝖣𝗂𝗌𝗄 𝖲𝗉𝖺𝖼𝖾: <code>{total}</code>
🗳 𝖴𝗌𝖾𝖽 𝖲𝗉𝖺𝖼𝖾: <code>{used} ({disk_usage}%)</code>
📝 𝖥𝗋𝖾𝖾 𝖲𝗉𝖺𝖼𝖾: <code>{free}</code> """

    msg = await bot.send_message(chat_id=update.chat.id, text="__𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀...__", parse_mode=enums.ParseMode.MARKDOWN)         
    await msg.edit_text(text=ms_g, parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="**𝖡𝗈𝗍 𝖨𝗌 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀...🪄**", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**𝖡𝗈𝗍 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 ! 𝖱𝖾𝖺𝖽𝗒 𝖳𝗈 𝖬𝗈𝗏𝖾 𝖮𝗇 💯**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message((filters.command(["report"]) | filters.regex("@admins") | filters.regex("@admin")) & filters.group)
async def notify_admin(bot, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    administrators = []
    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if (
            chat_member.status == enums.ChatMemberStatus.ADMINISTRATOR
            or chat_member.status == enums.ChatMemberStatus.OWNER
    ):
        return await message.delete()
    async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    full_name = message.from_user.first_name + " " + message.from_user.last_name if message.from_user.last_name else message.from_user.first_name
    
    ist = pytz.timezone("Asia/Kolkata")
    report_time = datetime.datetime.now(pytz.utc).astimezone(ist).strftime("%I:%M:%S %p")
    report_date = datetime.datetime.now(pytz.utc).astimezone(ist).strftime("%d-%B-%Y")
    report_day = datetime.datetime.now(pytz.utc).astimezone(ist).strftime("%A")

    reply_message = f"<b><i>✅ Rᴇᴩᴏʀᴛ Sᴇɴᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟ ✅</i></b>\n\n"
    reply_message += f"<b>👤 Rᴇᴘᴏʀᴛᴇᴅ ᴜsᴇʀ: {message.from_user.username}\n"
    reply_message += f"🆔 Rᴇᴘᴏʀᴛᴇᴅ ᴜsᴇʀ ɪᴅ: {message.from_user.id}\n"
    reply_message += f"📝 Rᴇᴘᴏʀᴛ ᴛʀᴀᴄᴋ ɪᴅ: [#TG8836467]({message.link})\n\n"
    reply_message += f"💬 Rᴇᴘᴏʀᴛ ᴛᴇxᴛ: {message.reply_to_message.text if message.reply_to_message else message.text.split(' ', 1)[1]}\n\n"
    reply_message += f"⏲️ Rᴇᴘᴏʀᴛ ᴛɪᴍᴇ: {report_time}\n"
    reply_message += f"🗓️ Rᴇᴘᴏʀᴛ ᴅᴀᴛᴇ: {report_date}\n"
    reply_message += f"⛅ Rᴇᴘᴏʀᴛ ᴅᴀʏ: {report_day}</b>"

    report = message.reply_to_message if message.reply_to_message else message
    m = await message.reply_text(reply_message, disable_web_page_preview=True)
    await asyncio.sleep(10)
    await m.delete()
    await message.delete()
    for admin in administrators:
        try:
            if admin.user.id != message.from_user.id:
                await bot.send_message(
                    chat_id=admin.user.id, 
                    text=f"⚠️ ATTENTION!\n\n<a href=tg://user?id={user_id}>{full_name}</a> Hᴀꜱ Rᴇǫᴜɪʀᴇᴅ Aɴ Aᴅᴍɪɴ Aᴄᴛɪᴏɴ Iɴ Tʜᴇ Gʀᴏᴜᴘ: {message.chat.title}\n\n[👉🏻 Go to message]({message.link})",
                    disable_web_page_preview=True
                )
        except:
            pass
            pass

@Client.on_message(filters.command("textlogs") & filters.user(ADMINS))
async def getlogss(bot, message):
    log = app.get_log(lines=10)
    await message.reply_text(text=f"{log}")
