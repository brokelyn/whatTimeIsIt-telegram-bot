from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from repo.group_repo import GroupRepo


class GroupController:

    @staticmethod
    def group_selection(bot, replay_chat_id, callback_pattern: str, callback_arg: str):
        groups = GroupRepo.findAll()

        if len(groups) == 0:
            bot.send_message(chat_id=replay_chat_id,
                             text="There are no group registered yet.")
        else:
            inline_keyboard = []
            for group in groups:
                callback_data = callback_pattern + " group " + str(callback_arg) + " " + str(group.id)
                inline_keyboard.append([InlineKeyboardButton(group.title, callback_data=callback_data)])
            bot.send_message(chat_id=replay_chat_id,
                             text="Choose one of the groups for that action",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard))
