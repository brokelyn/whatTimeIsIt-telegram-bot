from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from repo.group_repo import GroupRepo
import service.util_service as UtilService


class GroupController:

    @staticmethod
    def group_selection(bot, reply_chat_id, callback_pattern: str, callback_arg: str):
        groups = GroupRepo.findAll()

        if len(groups) == 0:
            bot.send_message(chat_id=reply_chat_id,
                             text="There are no group registered yet.")
        else:
            inline_keyboard = []
            for group in groups:
                callback_data = callback_pattern + " group " + str(callback_arg) + " " + str(group.id)
                inline_keyboard.append([InlineKeyboardButton(group.title, callback_data=callback_data)])
            bot.send_message(chat_id=reply_chat_id,
                             text="Choose one of the groups for that action",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard))

    @staticmethod
    def display_groups(update, context):
        if update.message.chat.type == 'private':
            groups = GroupRepo.findAll()

            reply_text = "Groups known by the bot:\n\n"
            for i in range(len(groups)):
                reply_text += str(i + 1) + ".   " + groups[i].title + "\n"
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=reply_text)
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Cannot list groups in groups...")

    @staticmethod
    def group_settings(update, context):
        msg = update.message

        if UtilService.is_private_chat(msg, context.bot):
            return

        group = GroupRepo.get_or_create(msg.chat.id, msg.chat.title)

        keyboard = list()

        text = "Violation Action:  " + group.violation_action
        callback_data = "settings violation_action"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

        text = "Timezone:  " + group.timezone
        callback_data = "settings timezone"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

        text = "Show Invite Link"
        callback_data = "settings invite_link"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

        context.bot.send_message(chat_id=msg.chat_id,
                                 text="Group: " + group.title,
                                 reply_markup=InlineKeyboardMarkup(keyboard))
