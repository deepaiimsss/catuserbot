from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from userbot import catub
from ..core.managers import edit_or_reply
from ..helpers.utils import get_user_from_event
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "admin"


@catub.cat_cmd(
    pattern=r"gpromote(?:\s|$)([\s\S]*)",
    command=("gpromote", plugin_category),
    info={
        "header": "Globally promotes a user in all groups where you are admin.",
        "usage": [
            "{tr}gpromote <userid/username/reply>",
            "{tr}gpromote <userid/username/reply> <custom title>",
        ],
    },
)
async def gpromote(event):
    "To globally promote a person in all groups"
    user, rank = await get_user_from_event(event)
    if not user:
        return
    if not rank:
        rank = "Admin"
    me = await event.client.get_me()
    if user.id == me.id:
        return await edit_or_reply(event, "U want to promote urself 😑😑 waao..")

    catevent = await edit_or_reply(event, "`Promoting globally...`")

    rgt = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    i = 0
    dialogs = await event.client.get_dialogs()
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            try:
                await event.client(EditAdminRequest(dialog.entity.id, user.id, rgt, rank))
                i += 1
                if i % 5 == 0:
                    await catevent.edit(f"**Promoting globally...**\n`Promoted in {i} chats`")
            except Exception:
                pass

    await catevent.edit(
        f"**Globally Promoted** [{user.first_name}](tg://user?id={user.id})\n**Custom Title:** `{rank}`\n**Total Chats:** `{i}`"
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#GPROMOTE\n"
            f"**User:** [{user.first_name}](tg://user?id={user.id})\n"
            f"**Custom Title:** `{rank}`\n"
            f"**Promoted in:** `{i} chats`",
        )


@catub.cat_cmd(
    pattern=r"gdemote(?:\s|$)([\s\S]*)",
    command=("gdemote", plugin_category),
    info={
        "header": "Globally demotes a user (removes admin rights) in all groups.",
        "usage": [
            "{tr}gdemote <userid/username/reply>",
        ],
    },
)
async def gdemote(event):
    "To globally demote a person in all groups"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    me = await event.client.get_me()
    if user.id == me.id:
        return await edit_or_reply(event, "U want to demote urself 😑😑 waao..")

    catevent = await edit_or_reply(event, "`Demoting globally...`")

    rgt = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )

    i = 0
    dialogs = await event.client.get_dialogs()
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            try:
                await event.client(EditAdminRequest(dialog.entity.id, user.id, rgt, "admin"))
                i += 1
                if i % 5 == 0:
                    await catevent.edit(f"**Demoting globally...**\n`Demoted in {i} chats`")
            except Exception:
                pass

    await catevent.edit(
        f"**Globally Demoted** [{user.first_name}](tg://user?id={user.id})\n**Total Chats:** `{i}`"
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#GDEMOTE\n"
            f"**User:** [{user.first_name}](tg://user?id={user.id})\n"
            f"**Demoted in:** `{i} chats`",
        )
