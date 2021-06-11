

def is_private_chat(msg, bot):
    if msg.chat.type == 'private':
        bot.send_message(chat_id=msg.chat_id, text="Feature only for group chats!")
        return True
    return False
