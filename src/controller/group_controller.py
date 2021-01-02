from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from repo.group_repo import GroupRepo


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
                                     text="Your are in a group...")
