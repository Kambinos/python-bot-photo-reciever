import telebot
from datetime import datetime, timedelta
from datetime import datetime, date, timedelta


ADMIN_ID = '' # TELEGRAM's ADMIN's ID
admin_id = '' # TELEGRAM's ADMIN's ID

bot = telebot.TeleBot('') # BOT TOKEN


users = {}

last_photo_time = {}  # словарь для хранения времени последней отправки фото от каждого пользователя
last_video_time = {}  # словарь для хранения времени последней отправки фото от каждого пользователя


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '') # write your description in '' when user start's bot it sends it description
    admin_id = '', # TELEGRAM's ADMIN's ID
    users[message.chat.id] = message.chat.first_name
    user_link = f'<a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>'
    bot.send_message(admin_id, f"Зарегестрировался новый пользователь: {user_link}", parse_mode='HTML')


@bot.message_handler(content_types=['photo'])
def receive_photo(message):
    file_id = message.photo[-1].file_id
    admin_id = 1, # TELEGRAM's ADMIN's ID without ''
    users[message.chat.id] = message.chat.first_name
    user_link = f'<a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>'
    user_id = message.from_user.id
    if user_id in last_photo_time:
        if datetime.now() - last_photo_time[user_id] < timedelta(days=1):
            bot.reply_to(message, "Вы можете отправить фото только один раз в 24 часа.") # user can send only one photo in 24 hours when bot is active
            return
    last_photo_time[user_id] = datetime.now()

    bot.reply_to(message, "") # write your description in '', when user sends photo it sends description
    bot.send_photo(admin_id, file_id, caption=f'Получено изображение от пользователя {user_link}', parse_mode='HTML')


@bot.message_handler(content_types=['video'])
def handle_video(message):
    if message.from_user.id == admin_id:
        return
    user_name = message.from_user.first_name or message.from_user.username
    users[message.chat.id] = message.chat.first_name
    user_link = f'<a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>'
    today = date.today()
    user_id = message.from_user.id
    if user_id in last_video_time:
        if datetime.now() - last_video_time[user_id] < timedelta(days=1):
            bot.reply_to(message, "Вы можете отправить фото только один раз в 24 часа.")
            return
    last_video_time[user_id] = datetime.now()

    bot.reply_to(message, "") # write your description in '', when user sends video it sends description
    bot.send_message(admin_id, f'A video note has been sent to the bot by {user_link} ', parse_mode='HTML')
    bot.send_video_note(admin_id, message.video.file_id)

if __name__ == '__main__':
    bot.polling(non_stop=True)






