# By @FeelDeD
from userbot import catub
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "useless"


async def isong(deep, text):
    if deep.fwd_from:
        return
    bot = "DeezerMusicBot"
    try:
        run = await deep.client.inline_query(bot, text)
        if run:
            result = await run[0].click("me")
        else:
            result = ""
    except Exception:
        result = ""
    return result


@catub.cat_cmd(
    pattern="isong ?(.*)",
    command=("isong", plugin_category),
    info={
        "header": "Inline song downloader by feelded",
        "usage": [
            "{tr}isong <song name>",
        ],
    },
)
async def main(deep):
    "I Song Downloader"
    text = deep.pattern_match.group(1)
    if not text:
        return await edit_delete(deep, "`Give me a song name`", 6)

    reply_to_id = await reply_id(deep)
    catevent = await edit_or_reply(deep, "`Searching for song...`")
    result = await isong(deep, text)
    if not result:
        return await edit_delete(catevent, f"`No result found for {text}`", 6)

    await catevent.delete()
    await deep.client.send_message(deep.chat_id, result, reply_to=reply_to_id)
    await result.delete()
