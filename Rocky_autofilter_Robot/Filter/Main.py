# (c) KICCHA REQUEST
from Config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, TUTORIAL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from OMDB import get_movie_info
import re
from pyrogram.errors import UserNotParticipant
from Rocky_autofilter_Robot import get_filter_results, get_file_details, is_subscribed, get_poster
from Rocky_autofilter_Robot import RATING, GENRES, HELP, ABOUT
import random
import asyncio
BUTTONS = {}
BOT = {}

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**𝙿𝚕𝚎𝚊𝚜𝚎 𝙲𝚕𝚎𝚌𝚔 𝚃𝚑𝚒𝚜 𝙱𝚞𝚝𝚝𝚘𝚗 𝙹𝚘𝚒𝚗 𝙼𝚢 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 𝙰𝚗𝚍 𝙲𝚕𝚎𝚌𝚔 𝚃𝚛𝚢 𝙰𝚐𝚊𝚒𝚗 𝙱𝚞𝚝𝚝𝚘𝚗 𝙰𝚗𝚍 𝚃𝚊𝚔𝚎 𝚈𝚘𝚞𝚛 𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝙼𝚘𝚟𝚒𝚎 𝚄𝚜𝚎 𝚃𝚑𝚒𝚜 𝙱𝚘𝚝...!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 𝙹𝚘𝚒𝚗 𝙼𝚢 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 🤖", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    title = message.text
    movie_info = get_movie_info(title) 
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        mo_tech_yt = f"**👤 ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝔹𝕪:☞** {message.from_user.mention}\n┏━━━━━━━━━━━━━━━━\n┣🗂️ 𝐓𝐢𝐭𝐥𝐞:☞ {search}\n┣\n┣⭐ 𝙍𝙖𝙩𝙞𝙣𝙜:☞ {random.choice(RATING)}\n┣\n┣🎭 𝑮𝒆𝒏𝒓𝒆:☞ {random.choice(GENRES)}\n┣\n┗━━━━━━━━━━━━━━━━\n\n\n**📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍 𝙱𝚢:☞ {message.chat.title}\n\n✪༺ ──•◈•─ ─•◈•──༻✪"
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"sachin9742s#{file_id}")]
                    )
        else:
            await client.send_photo(
            chat_id = message.chat.id,
            photo="https://telegra.ph/file/328fc84d36e29e7b42869.jpg",
 caption="<b>Couldn't Find This Movie.Try Again..! And Admins will add it Soon 🔜🥺</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📞 Contact Admin", url='t.me/sachin_official_admin')
                    ]
                ]
            )
        )
            return

        if not btn:
            return

        if len(btn) > 5: 
            btns = list(split_list(btn, 5)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🎶 𝙿𝚊𝚐𝚎𝚜 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_photo(photo="https://telegra.ph/file/392b4ecbb4f9d8be8482a.jpg", caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text=f"🎶 𝙿𝚊𝚐𝚎𝚜 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton(text="≫ 𝑵𝒆𝒙𝒕 ≫",callback_data=f"next_0_{keyword}")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    title = message.text
    movie_info = get_movie_info(title) 
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        mo_tech_yt = f"**👤 ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝔹𝕪:☞** {message.from_user.mention}\n┏━━━━━━━━━━━━━━━━\n┣🗂️ 𝐓𝐢𝐭𝐥𝐞:☞ {search}\n┣\n┣⭐ 𝙍𝙖𝙩𝙞𝙣𝙜:☞ {random.choice(RATING)}\n┣\n┣🎭 𝑮𝒆𝒏𝒓𝒆:☞ {random.choice(GENRES)}\n┣\n┗━━━━━━━━━━━━━━━━\n\n\n**📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍 𝙱𝚢:☞ {message.chat.title}\n\n✪༺ ──•◈•─ ─•◈•──༻✪"
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=sachin9742s_-_-_-_{file_id}"),
                     InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'files_#{file.file_id}',)]
                )
        else:
            Rocky_autofilter_Robot=await client.send_message(
            chat_id = message.chat.id,
            text=f"""
                 ✋𝙷𝙸 {message.from_user.mention} 𝚂𝚘𝚛𝚛𝚢, 𝙽𝚘 𝙼𝚘𝚟𝚒𝚎 𝚁𝚎𝚕𝚊𝚝𝚎𝚍 𝚃𝚘 𝚃𝚑𝚎 𝙶𝚒𝚟𝚎𝚗 𝚆𝚘𝚛𝚐 𝚆𝚊𝚜 𝙵𝚘𝚞𝚗𝚍 🥺

<b>Admins Will Add It Soon </b> 

𝙿𝚕𝚎𝚊𝚜𝚎 𝙲𝚕𝚒𝚌𝚔 𝙱𝚞𝚝𝚝𝚘𝚗 𝚃𝚘 𝙸𝚖𝚍𝚋 𝙶𝚘𝚘𝚐𝚕𝚎 𝙰𝚗𝚍 𝙲𝚘𝚗𝚏𝚒𝚛𝚖 𝚃𝚑𝚎 𝙲𝚘𝚛𝚛𝚎𝚌𝚝 𝚂𝚙𝚎𝚕𝚕𝚒𝚗𝚐 𝙿𝚕𝚎𝚊𝚜𝚎 🙏 """,
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup( 
                [ 
                    [ 
                         InlineKeyboardButton("🔍 Search Google 🔎", url='https://www.imdb.com/search/') 
                    ] 
                ] 
           ) 
        )
            await asyncio.sleep(10) # in seconds 
            await Rocky_autofilter_Robot.delete()
            return
        if not btn:
            return

        if len(btn) > 5: 
            btns = list(split_list(btn, 5)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🎶 𝙿𝚊𝚐𝚎𝚜 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo="https://telegra.ph/file/392b4ecbb4f9d8be8482a.jpg", caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="≫ 𝑵𝒆𝒙𝒕 ≫",callback_data=f"next_0_{keyword}"),
             InlineKeyboardButton(text=f"🎶 𝙿𝚊𝚐𝚎𝚜 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(mo_tech_yt, reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⌫ 𝐁𝐚𝐜𝐤", callback_data=f"back_{int(index)+1}_{keyword}")]
                    [InlineKeyboardButton(f"🎶 𝙿𝚊𝚐𝚎𝚜 {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⌫ 𝐁𝐚𝐜𝐤", callback_data=f"back_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton(f"🗓️ {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("≫ 𝑵𝒆𝒙𝒕 ≫", callback_data=f"next_{int(index)+1}_{keyword}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("≫ 𝑵𝒆𝒙𝒕 ≫", callback_data=f"next_{int(index)-1}_{keyword}")]
                    [InlineKeyboardButton(f"🎶 𝙿𝚊𝚐𝚎𝚜 {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⌫ 𝐁𝐚𝐜𝐤", callback_data=f"back_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton(f"🗓️ {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("≫ 𝑵𝒆𝒙𝒕 ≫", callback_data=f"next_{int(index)+1}_{keyword}")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "help":
            buttons = [
                [
                    InlineKeyboardButton('💬 𝙲𝚑𝚊𝚗𝚗𝚎𝚕', url='https://t.me/gd_film'),
                    InlineKeyboardButton('🗣️ 𝙶𝚛𝚘𝚞𝚙', url=f'https://t.me/KicchaRequest')
                ],
                [
                    InlineKeyboardButton("🧑‍💻 𝙼𝚢 𝙱𝚘𝚜𝚜", url="https://t.me/sachin_official_admin"),
                    InlineKeyboardButton("𝙰𝚋𝚘𝚞𝚝 🤠", callback_data="about")
                ]
                ]
            await query.message.edit(text=f"{HELP}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('💬 𝙲𝚑𝚊𝚗𝚗𝚎𝚕', url='https://t.me/gd_film'),
                    InlineKeyboardButton('🗣️ 𝙶𝚛𝚘𝚞𝚙', url=f'https://t.me/KicchaRequest')
                ],
                [
                    InlineKeyboardButton("🤔 𝙷𝚎𝚕𝚙", callback_data="help"),
                    InlineKeyboardButton("🧑‍💻 𝙼𝚢 𝙱𝚘𝚜𝚜", url="https://t.me/sachin_official_admin"),
                ]
                ]
            await query.message.edit(text=f"{ABOUT}", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)


        elif query.data.startswith("sachin9742s"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('🗣️ 𝙶𝚛𝚘𝚞𝚙', url=f'https://t.me/KicchaRequest'),
                        InlineKeyboardButton('Update Channel', url='https://t.me/KR_ROCKERS_DVD_WEB_OTT_MOVIES')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('🗣️ 𝙶𝚛𝚘𝚞𝚙', url=f'https://t.me/KicchaRequest'),
                        InlineKeyboardButton('Update Channel', url='https://t.me/KR_ROCKERS_DVD_WEB_OTT_MOVIES')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("Nice Try With You Don't Asking Me👀",show_alert=True)
