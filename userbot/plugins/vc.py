# By @deepaiims
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.phone import CreateGroupCallRequest, DiscardGroupCallRequest, GetGroupCallRequest

from userbot import catub
from ..core.managers import edit_or_reply

plugin_category = "tools"


async def getvc(deep):
    try:
        chat_ = await deep.client(GetFullChannelRequest(deep.chat_id))
        if not chat_.full_chat.call:
            return None
        _chat = await deep.client(GetGroupCallRequest(chat_.full_chat.call, limit=0))
        return _chat.call
    except Exception:
        return None


@catub.cat_cmd(
    pattern="startvc$",
    command=("startvc", plugin_category),
    info={
        "header": "Start Voice Chat in the group.",
        "usage": [
            "{tr}startvc",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def start_vc(deep):
    "Start voicechat"
    try:
        await deep.client(CreateGroupCallRequest(deep.chat_id))
        await edit_or_reply(deep, "`Voice Chat Started Successfully`")
    except Exception as e:
        await edit_or_reply(deep, f"`Error starting Voice Chat:`\n`{str(e)}`")


@catub.cat_cmd(
    pattern="endvc$",
    command=("endvc", plugin_category),
    info={
        "header": "End Voice Chat in the group.",
        "usage": [
            "{tr}endvc",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def end_vc(deep):
    "End voicechat"
    try:
        vc_call = await getvc(deep)
        if not vc_call:
            return await edit_or_reply(deep, "`No active Voice Chat found in this chat.`")
        await deep.client(DiscardGroupCallRequest(vc_call))
        await edit_or_reply(deep, "`Voice Chat Ended Successfully`")
    except Exception as e:
        await edit_or_reply(deep, f"`Error ending Voice Chat:`\n`{str(e)}`")
