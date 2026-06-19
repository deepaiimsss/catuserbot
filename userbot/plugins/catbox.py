from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from ..helpers.utils import reply_id

plugin_category = "utils"


@catub.cat_cmd(
    pattern="ctm$",
    command=("ctm", plugin_category),
    info={
        "header": "Upload media to Catbox via @CatBoxyBot",
        "description": "Reply to any media (photo, document, video, sticker, gif, audio, voice) with this command to upload it to Catbox and get the link.",
        "usage": "{tr}ctm",
    },
)
async def _(event):
    "Upload media to Catbox."
    reply_to = await reply_id(event)
    replied = await event.get_reply_message()
    if not replied or not replied.media:
        return await edit_delete(event, "`Reply to a media message to upload to Catbox`", 10)

    chat = "@CatBoxyBot"
    catevent = await edit_or_reply(event, "`Uploading to Catbox via @CatBoxyBot...`")

    async with event.client.conversation(chat) as conv:
        try:
            msg_flag = await conv.send_file(replied.media)
        except YouBlockedUserError:
            await edit_or_reply(catevent, "**Error:** Trying to unblock @CatBoxyBot & retry, wait a sec...")
            await catub(unblock("CatBoxyBot"))
            msg_flag = await conv.send_file(replied.media)

        try:
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await catevent.delete()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to)
        except Exception as e:
            await edit_or_reply(catevent, f"**Error:** `{e}`")
        finally:
            await delete_conv(event, chat, msg_flag)
