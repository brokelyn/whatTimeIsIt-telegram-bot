from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from repo.group_repo import GroupRepo
import service.util_service as UtilService
import service.group_service as GroupService


class GroupController:

    @staticmethod
    async def group_selection(bot, reply_chat_id, callback_pattern: str, callback_arg: str):
        groups = GroupRepo.findAll()

        if len(groups) == 0:
            await bot.send_message(chat_id=reply_chat_id,
                             text="There are no group registered yet.")
        else:
            inline_keyboard = []
            for group in groups:
                callback_data = callback_pattern + " group " + str(callback_arg) + " " + str(group.id)
                inline_keyboard.append([InlineKeyboardButton(group.title, callback_data=callback_data)])
            await bot.send_message(chat_id=reply_chat_id,
                             text="Choose one of the groups for that action",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard))

    @staticmethod
    async def display_groups(update, context):
        if update.message.chat.type == 'private':
            groups = GroupRepo.findAll()

            reply_text = "Groups known by the bot:\n\n"
            for i in range(len(groups)):
                reply_text += str(i + 1) + ".   " + groups[i].title + "\n"
            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text=reply_text)
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text="Cannot list groups in groups...")

    @staticmethod
    async def group_settings_callback(update, context):
        group_id = update.callback_query.message.chat.id
        query_sections = update.callback_query.data.split(" ")
        command = query_sections[1] if len(query_sections) > 1 else ""
        group = GroupRepo.get_or_none(group_id)

        text = "Group: " + group.title + "\n"
        keyboard = GroupService.group_settings_keyboard(group)

        if command == "violation_action":
            group = GroupService.change_violation_action(group_id)
            keyboard = GroupService.group_settings_keyboard(group)

        elif command == "invite_link":
            text = "Group invite link: " + group.invite_link
            keyboard = None

        elif command == "select_timezone":
            if len(query_sections) > 2:
                keyboard = GroupService.timezone_keyboard(query_sections[2])
            else:
                keyboard = GroupService.timezone_keyboard()
            text = "Select a new timezone: \n"

        elif command == "auto_events":
            group = GroupService.change_auto_events(group_id)
            keyboard = GroupService.group_settings_keyboard(group)

        elif command == "set_timezone":
            group = GroupService.set_timezone(group_id, query_sections[2], context.job_queue)
            keyboard = GroupService.group_settings_keyboard(group)

        await update.callback_query.message.edit_text(text=text,
                                                reply_markup=keyboard)

    @staticmethod
    async def group_settings(update, context):
        msg = update.message

        if UtilService.is_private_chat(msg, context.bot):
            return

        group = GroupRepo.get_or_create(msg.chat.id, msg.chat.title)

        keyboard = GroupService.group_settings_keyboard(group)

        await context.bot.send_message(chat_id=msg.chat_id,
                                 text="Group: " + group.title,
                                 reply_markup=keyboard)
