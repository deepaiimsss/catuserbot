import os

import requests

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "utils"


@catub.cat_cmd(
    pattern="ctm$",
    command=("ctm", plugin_category),
    info={
        "header": "Upload media to Catbox.moe",
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

    catevent = await edit_or_reply(event, "`Downloading media...`")
    
    try:
        downloaded_file_name = await event.client.download_media(replied.media)
    except Exception as e:
        return await edit_or_reply(catevent, f"**Error downloading:** `{e}`")

    await edit_or_reply(catevent, "`Uploading to Catbox.moe...`")
    
    try:
        url = "https://catbox.moe/user/api.php"
        data = {"reqtype": "fileupload"}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        with open(downloaded_file_name, "rb") as f:
            files = {"fileToUpload": f}
            response = requests.post(url, data=data, files=files, headers=headers, timeout=150)
            
        if response.status_code == 200:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.text, reply_to=reply_to)
        else:
            await edit_or_reply(
                catevent, 
                f"**Error:** `Failed to upload, status code {response.status_code}`\n**Response:** `{response.text[:200]}`"
            )
    except Exception as e:
        await edit_or_reply(catevent, f"**Error:** `{e}`")
    finally:
        if downloaded_file_name and os.path.exists(downloaded_file_name):
            os.remove(downloaded_file_name)
