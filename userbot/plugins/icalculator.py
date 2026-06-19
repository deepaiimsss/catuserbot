# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# Original file can be found at https://github.com/TeamUltroid/Ultroid/blob/main/plugins/calculator.py
# Ported to cat userbot by @realnub. If you remove these three lines then you are a pure 100% gay, real idiot and you will die in hell for sure.

import re

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery

from userbot import catub
from ..Config import Config
from ..core.decorators import check_owner

CALC = {}

plugin_category = "utils"

m = [
    "AC",
    "C",
    "⌫",
    "%",
    "7",
    "8",
    "9",
    "+",
    "4",
    "5",
    "6",
    "-",
    "1",
    "2",
    "3",
    "x",
    "00",
    "0",
    ".",
    "÷",
]
tultd = [Button.inline(f"{x}", data=f"calc{x}") for x in m]
lst = list(zip(tultd[::4], tultd[1::4], tultd[2::4], tultd[3::4]))
lst.append([Button.inline("=", data="calc=")])


@catub.cat_cmd(
    pattern="icalc(?:\s|$)([\s\S]*)",
    command=("icalc", plugin_category),
    info={
        "header": "Inline Calculator.",
        "usage": "{tr}icalc",
        "description": "An awesome inline calculator with cool buttons.",
    },
)
async def icalc_cmd(e):
    is_bot = getattr(e.client, "_bot", False)
    if not is_bot:
        try:
            is_bot = await e.client.is_bot()
        except Exception:
            is_bot = False
    if is_bot:
        return await e.reply("**INLINE CAT CALCULATOR**", buttons=lst)
    results = await e.client.inline_query(Config.TG_BOT_USERNAME, "calc")
    await results[0].click(e.chat_id, silent=True, hide_via=True)
    await e.delete()


@catub.tgbot.on(InlineQuery)
async def inlinecalc(event):
    query_user_id = event.sender_id
    query = event.text
    string = query.lower()
    if (
        query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS
    ) and string == "calc":
        calc = event.builder.article(
            "Calc", text="**INLINE CAT CALCULATOR**", buttons=lst
        )
        await event.answer([calc])


@catub.tgbot.on(CallbackQuery(data=re.compile(b"calc(.*)")))
@check_owner
async def calc_callback(e):  # sourcery no-metrics
    x = (e.data_match.group(1)).decode()
    user = e.sender_id
    get = None
    if x == "AC":
        CALC.pop(user, None)
        await e.edit(
            "**INLINE CAT CALCULATOR**",
            buttons=[Button.inline("Open Again", data="recalc")],
        )
    elif x == "C":
        CALC.pop(user, None)
        await e.answer("Cleared")
    elif x == "⌫":
        if CALC.get(user):
            get = CALC[user]
        if get:
            new_val = get[:-1]
            CALC[user] = new_val
            await e.answer(new_val or "Cleared")
        else:
            await e.answer("Cleared")
    elif x == "%":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC[user] = get + "/100"
            await e.answer(get + "/100")
    elif x == "÷":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC[user] = get + "/"
            await e.answer(get + "/")
    elif x == "x":
        if CALC.get(user):
            get = CALC[user]
        if get:
            CALC[user] = get + "*"
            await e.answer(get + "*")
    elif x == "=":
        if CALC.get(user):
            get = CALC[user]
        if get:
            if get.endswith(("*", ".", "/", "-", "+")):
                get = get[:-1]
            try:
                # Sanitization check to prevent any arbitrary code execution
                if not all(char in "0123456789+-*/. %()" for char in get):
                    raise ValueError("Unsafe characters detected")
                out = eval(get)
                num = float(out)
                if num.is_integer():
                    num = int(num)
                await e.answer(f"Answer : {num}", cache_time=0, alert=True)
                CALC[user] = str(num)
            except Exception:
                CALC.pop(user, None)
                await e.answer("Error", cache_time=0, alert=True)
        else:
            await e.answer("None")
    else:
        if CALC.get(user):
            get = CALC[user]
        else:
            get = ""
        CALC[user] = get + x
        await e.answer(get + x)


@catub.tgbot.on(CallbackQuery(data=re.compile(b"recalc")))
@check_owner
async def recalc_callback(e):
    await e.edit("**𝙎𝙀𝙓𝙔 𝘾𝘼𝙏 𝘾𝘼𝙇𝘾𝙐𝙇𝘼𝙏𝙊𝙍**", buttons=lst)
