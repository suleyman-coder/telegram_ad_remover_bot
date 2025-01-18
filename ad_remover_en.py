import telebot
import time

bot_token = 'enter your bot token'
bot = telebot.TeleBot(bot_token)
reklam_gonderildi=False
@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, "Hello! I am Gruop ad remover bot and I was created by @fullstackofdeveloper and if you add me to your chat and make me an admin, I can remove ads❗ If you want to learn how to use it in a group, type bot_info")

@bot.message_handler(commands=["stat"])
def get_stats(message):
    users_count = bot.get_chat_members_count(message.chat.id)
    active_users = bot.get_chat_administrators(message.chat.id)

    stats_message = f" User count: {users_count}\nActive members: {', '.join([user.user.username for user in active_users])}"
    bot.reply_to(message, stats_message)

@bot.message_handler(commands=['remove_ban'])
def remove_ban_command(message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)

    if chat_member.status in ['administrator', 'creator']:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = ' '.join(message.text.split()[1:])

        bot.unban_chat_member(message.chat.id, user_id)

        bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_id}</a> ban removed", parse_mode='HTML')
    else:
        bot.reply_to(message, "You must be an admin to use this command.")

@bot.message_handler(commands=['get_mention'])
def agza_nick(message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)

    if chat_member.status == 'administrator':
        if message.reply_to_message is not None:
            user_id = message.reply_to_message.from_user.id
            bot.send_message(message.chat.id, f"[{user_id}](tg://user?id={user_id}) Mention", parse_mode='Markdown')
        else:
            bot.reply_to(message, "You need to reply to a message and write get_mention, otherwise it won't work")
    else:
        bot.reply_to(message, "Only admins can use it")

@bot.message_handler(commands=['ban'])
def ban_command(message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)

    if chat_member.status in ['administrator', 'creator']:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        else:
            user_id = ' '.join(message.text.split()[1:])

        bot.kick_chat_member(message.chat.id, user_id)

        bot.send_message(message.chat.id, f"<a href='tg://user?id={user_id}'>{user_id}</a> banned", parse_mode='HTML')
    else:
        bot.reply_to(message, "You must be an admin to use this command.")

@bot.message_handler(func=lambda message: message.text.lower() == "hello")
def reply_salam(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello, welcome to the group")

@bot.message_handler(func=lambda message: message.text.lower() == "user_info")
def reply_info(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_info = f"[{user_name}](tg://user?id={user_id})"
    bot.send_message(chat_id, user_info, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text.lower() == "bot_info")
def reply_feature(message):
    chat_id = message.chat.id

    features = [
        "Bot's responding messages:",
        "Hello",
        "user_info",
        "Commands and messages for admins",
        "/ban - removes from the group by banning",
        "mute - mutes so they can't send messages",
        "unmute - unmutes so they can send messages",
        "/remove_ban - removes bans from members",
        "/get_mention - Sends the member's mention as blue text",
        "bot_info - Sends the bot's usage"
    ]

    features_list = "\n".join(features)
    bot.send_message(chat_id, f"About the bot:\n\n{features_list}")

@bot.message_handler(func=lambda message: message.text.lower() == 'mute')
def mute(message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)

    if chat_member.status in ['administrator', 'creator']:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.reply_to_message.chat.id
        else:
            user_id = ' '.join(message.text.split()[1:])
            chat_id = message.chat.id

        bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)

        bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_id}</a> muted", parse_mode='HTML')
    else:
        bot.reply_to(message, "Only admins can use it")

@bot.message_handler(func=lambda message: message.text.lower() == 'unmute')
def unmute(message):
    chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)

    if chat_member.status in ['administrator', 'creator']:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_id = message.reply_to_message.chat.id
        else:
            user_id = ' '.join(message.text.split()[1:])
            chat_id = message.chat.id

        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)

        bot.send_message(chat_id, f"<a href='tg://user?id={user_id}'>{user_id}</a> unmuted", parse_mode='HTML')
    else:
        bot.reply_to(message, "Only admins can use it")

@bot.message_handler(func=lambda message: message.chat.type == "supergroup")
def handle_group_message(message):
    if any(word in message.text.lower() for word in ['http://', 'https://', 't.me/', '@','pubg']):
        if message.forward_from_chat:
            bot.reply_to(message, "This is an ad from this channel")
            return
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ['administrator', 'creator']:
            bot.reply_to(message, f"{message.from_user.first_name}, advertising is prohibited.")
            bot.delete_message(message.chat.id, message.message_id)
            bot.kick_chat_member(message.chat.id, message.from_user.id)
            bot.send_message(message.chat.id, f"User ID: {message.from_user.id}", parse_mode='HTML')
            bot.send_message(message.chat.id, "<b>Do not advertise❗</b>", parse_mode='HTML')
            bot.send_message(message.chat.id, f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> advertised and got banned.", parse_mode='HTML')

@bot.message_handler(commands=['member_transfer'])
def handle_member_transfer(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id != 5138836209:
        bot.send_message(chat_id, "You must be the bot owner to use this command.")
        return

    bot.send_message(chat_id, "Send the group to get users from.")
    bot.register_next_step_handler(message, get_source_group)

def get_source_group(message):
    chat_id = message.chat.id
    source_group_id = message.text

    bot.send_message(chat_id, "Send the group to send users to.")
    bot.register_next_step_handler(message, get_destination_group, source_group_id)

def get_destination_group(message, source_group_id):
    chat_id = message.chat.id
    destination_group_id = message.text

    bot.send_message(chat_id, "Send the second group link.")
    bot.register_next_step_handler(message, transfer_members, source_group_id, destination_group_id)

def transfer_members(message, source_group_id, destination_group_id):
    chat_id = message.chat.id
    link = message.text

    source_group_admin = bot.get_chat_member(source_group_id, message.from_user.id).status == 'administrator'
    destination_group_admin = bot.get_chat_member(destination_group_id, message.from_user.id).status == 'administrator'

    if not source_group_admin or not destination_group_admin:
        bot.send_message(chat_id, "You are not an admin in one or both of the groups.")
        return

    members = []
    offset = 0
    limit = 40

    while True:
        response = bot.get_chat_members(source_group_id, limit=limit, offset=offset)
        for member in response:
            members.append(member.user.id)

        if len(response) < limit:
            break

        offset += limit

    if len(members) == 0:
        bot.send_message(chat_id, "There are no members in the source group.")
        return

    bot.add_chat_members(destination_group_id, members[:40])
    bot.send_message(chat_id, "Users were successfully added to the second group.")

@bot.message_handler(commands=['broadcast'])
def owner_command(message):
    global reklam_gonderildi
    owner_id = 5138836209
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id == owner_id and not reklam_gonderildi:
        reklam_mesaji = message.text.replace("/broadcast", "")
        bot.send_message(chat_id, "Sending advertisement...")
        user_ids = get_all_chat_member_ids(chat_id)
        for user_id in user_ids:
            bot.send_message(user_id, reklam_mesaji)
        reklam_gonderildi = True
        bot.send_message(chat_id, "Advertisement sent")
    elif user_id == owner_id and reklam_gonderildi:
        bot.send_message(chat_id, "Advertisement has already been sent.")
    else:
        bot.send_message(chat_id, "Only @fullstackofdeveloper can use it")

def get_all_chat_member_ids(chat_id):
    user_ids = []
    members = bot.get_chat_members(chat_id)
    for member in members:
        user_ids.append(member.user.id)
    return user_ids

@bot.message_handler(commands=['start', 'get_mention','remove_ban','ban','broadcast','stat','member_transfer'])
def handle_known_command(message):
    pass

@bot.message_handler(func=lambda message: message.text in ['bot_info', 'user_info','Hello','mute','unmute'])
def handle_known_message(message):
    pass

@bot.message_handler(func=lambda message: True)
def unknown_command_or_message(message):
    bot.reply_to(message, "You sent the wrong command or message. To see what the bot can do, type bot_info" )



@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_members(message):
    if message.chat.type == 'supergroup':
        for member in message.new_chat_members:
            if member.is_bot:
                bot.send_message(message.chat.id, f"Hello {member.first_name}! I am {bot.get_me().first_name}, a chatbot, and I can remove ads in the group. Just add me to your chat and make me an admin")
            else:
                bot.restrict_chat_member(message.chat.id, member.id, can_send_messages=True)
                bot.send_message(message.chat.id, f"Hello {member.first_name}! Sending advertisements in the group is not allowed. Do not advertise.")

@bot.message_handler(func=lambda message: True)
def handle_error(message):
    global error_occurred
    if error_occurred:
        bot.send_message(message.chat.id, 'There might be a wrong command used in the bot...')

        time.sleep(1)

        raise Exception('Bot gave an error')
    else:
        bot.send_message(message.chat.id, 'The bot is restarting, someone might have used the wrong command... Check your used command')

def run_bot():
    global error_occurred
    while True:
        try:
            bot.polling()
        except Exception as e:
            error_occurred = True
            print('Bot gave an error:', e)
            time.sleep(5)
            error_occurred = False

if __name__ == '__main__':
    run_bot()

bot.polling()
