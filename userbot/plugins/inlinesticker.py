import random

from userbot import catub
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "useless"


@catub.cat_cmd(
    pattern="ist ?(.*)",
    command=("ist", plugin_category),
    info={
        "header": "Inline Write-On Sticker",
        "examples": ["{tr}ist dead", "{tr}ist dead;0"],
        "usage": [
            "{tr}ist <your text>",
            "{tr}ist <your text>;<number 0/4>",
        ],
    },
)
async def ist(deep):
    "Some kinda shit"
    text = deep.pattern_match.group(1)
    if not text:
        return await edit_delete(deep, "`Give me a text`", 5)

    reply_to_id = await reply_id(deep)
    catevent = await edit_or_reply(deep, "`Processing...`")

    text = text.replace(" ", "-")
    if ";" in text:
        try:
            query, num = text.split(";")
            num = int(num)
        except ValueError:
            query = text
            num = random.choice(range(0, 4))
    else:
        query = text
        num = random.choice(range(0, 4))

    query = query.replace("-", " ")
    bot = "QuotAfBot"
    try:
        run = await deep.client.inline_query(bot, query)
        if not run:
            return await edit_delete(catevent, f"`No stickers found for: {query}`", 5)

        # Clamp number to valid range
        if num < 0 or num >= len(run):
            num = 0

        result = await run[num].click("me")
        if result:
            await deep.client.send_message(deep.chat_id, result, reply_to=reply_to_id)
            await catevent.delete()
            await result.delete()
        else:
            await edit_delete(catevent, "`Failed to get sticker.`", 5)
    except Exception as e:
        return await edit_delete(catevent, f"`Error:`\n`{str(e)}`", 6)
