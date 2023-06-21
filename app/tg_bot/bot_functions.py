import telebot
from environs import Env

from tg_bot.bot_markups import speaker_menu_markup, user_menu_markup, registrate_markup, accept_markup


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
bot = telebot.TeleBot(tg_bot_token)


def is_registered_user(chat_id):
    # TODO check user in db
    return False


def is_speaker(chat_id):
    # TODO check user status
    return True


def get_info(message: telebot.types.Message):
    # TODO add info
    bot.send_message(message.chat.id, f'Информация о нас')
    return


def get_schedule(message: telebot.types.Message):
    # TODO get schedule from db
    bot.send_message(message.chat.id, f'Расписание выступлений')
    return


def change_speaker():
    # TODO change speaker status
    return


def registrate_user(message: telebot.types.Message, step=0):
    # TODO Fix or rework
    if step == 0:
        msg = bot.send_message(message.chat.id, f'Введите ваше ФИО')
        bot.register_next_step_handler(msg, registrate_user, 1)
    if step == 1:
        msg = bot.send_message(message.chat.id, f'Ваше ФИО: {message.text}', reply_markup=accept_markup)
        if message.text == 'Подтвердить':
            # TODO save user fullname for next steps
            bot.register_next_step_handler(msg, registrate_user, 2)
        else:
            return
    if step == 2:
        msg = bot.send_message(message.chat.id, f'Введите вашу почту')
        bot.register_next_step_handler(msg, registrate_user, 3)
    if step == 3:
        msg = bot.send_message(message.chat.id, f'Ваша почта: {message.text}', reply_markup=accept_markup)
        if message.text == 'Подтвердить':
            # TODO save user mail for next steps
            bot.register_next_step_handler(msg, registrate_user, 4)
        else:
            return
    if step == 4:
        # TODO save user_mail, user_id, user_fullname in db
        bot.send_message(message.chat.id, 'Регистрация завершена. Используйте команду /start')
        return


def start_bot(message: telebot.types.Message):
    # msg = bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    user_id = message.from_user.id
    if is_registered_user(user_id):
        if is_speaker(user_id):
            bot.send_message(
                message.chat.id,
                f'Здравствуйте, {message.from_user.username}',
                reply_markup=speaker_menu_markup)
        else:
            bot.send_message(
                message.chat.id,
                f'Здравствуйте, {message.from_user.username}',
                reply_markup=user_menu_markup
            )
    else:
        bot.send_message(
            message.chat.id,
            f'Здравствуйте, {message.from_user.username}',
            reply_markup=registrate_markup
        )