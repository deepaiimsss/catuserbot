# Inline Ping by @deepaiims
import re
from datetime import datetime

from telethon import Button, events
from telethon.events import CallbackQuery

from ..Config import Config
from userbot import catub
from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "tools"


@catub.cat_cmd(
    pattern="iping$",
    command=("iping", plugin_category),
    info={
        "header": "Shows bot ping in inline mode",
        "usage": [
            "{tr}iping",
        ],
    },
)
async def iping_cmd(deep):
    "Inline Ping"
    reply_to_id = await reply_id(deep)
    try:
        results = await deep.client.inline_query(Config.TG_BOT_USERNAME, "ping")
        if results:
            await results[0].click(deep.chat_id, reply_to=reply_to_id, hide_via=True)
            await deep.delete()
        else:
            await edit_or_reply(deep, "`Inline ping failed - no results.`")
    except Exception as e:
        await edit_or_reply(deep, f"`Inline ping failed: {str(e)}`")


@catub.tgbot.on(events.InlineQuery(pattern=r"ping$"))
async def inline_ping_handler(event):
    from ..core.data import _sudousers_list
    sudo_users = _sudousers_list()
    if event.sender_id != catub.uid and event.sender_id not in sudo_users:
        return
    builder = event.builder
    result = builder.article(
        title="Inline Ping",
        description="Click here to send inline ping button",
        text="**Ping...**",
        buttons=[Button.inline("Ping ⚡", data="ping")],
    )
    await event.answer([result])


@catub.tgbot.on(CallbackQuery(data=re.compile(b"ping")))
async def ping(event):
    from ..core.data import _sudousers_list
    sudo_users = _sudousers_list()
    owner_id = Config.OWNER_ID or catub.uid
    if event.sender_id != owner_id and event.sender_id not in sudo_users and event.sender_id not in Config.SUDO_USERS:
        return await event.answer("You are not authorized to use this bot.", alert=True)

    start = datetime.now()
    await event.client.get_me()
    end = datetime.now()
    ms = round((end - start).total_seconds() * 1000, 3)
    ping_data = f"꧁☞︎︎︎𝐏𝐢𝐧𝐠꧂ {ms}ms"
    await event.answer(ping_data, cache_time=0, alert=True)
