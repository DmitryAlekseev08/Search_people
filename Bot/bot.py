from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, \
    CallbackContext
from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton, ParseMode
import logging.config

from telegram.utils.request import Request
# Подключение написанных модулей для html-запросов и валидации
from Request.request import vk_request
from Validate.validator import validator, replacing_sex, replacing_status

# Telegram
TB_TOKEN = '1111111111111111111111111111111111111111111111'
CHAT_ID = '111111111'

# Константы состояний
Q, CITY, SEX, AGE_FROM, AGE_TO, STATUS, COUNT = range(7)

# Настройка логирования
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("Your_assistant")

# Кнопки для клавиатуры
button_help = "/help"
button_know = "I don't know"
BUTTON_SEX = ['man', 'woman', 'any']
BUTTON_STATUS = ['not married (not married)', 'meets', 'engaged ', 'married',
                 "it's complicated", 'in active search', 'lover', 'in civil marriage']


# Обработчик команды /help
def command_help(update: Update, context: CallbackContext):
    logger.info("Help")
    update.message.reply_text(
        '🔻This program find people from social network, called VK.'
        '\nTo start print any text.'
        '\nTo get help print                       /help'
        '\nTo stop entering data print   /cancel',
    )


# Клавиатура с кнопкой /help
def reply_markup_help():
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help),
            ],
        ],
        resize_keyboard=True
    )
    return reply_markup


# Клавиатура с кнопкой "I don't know"
def reply_markup_know():
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_know),
            ],
        ],
        resize_keyboard=True
    )
    return reply_markup


# Стартовый обработчик
# После ввода команда /start управление переходит ConversationHandler
def echo_handler(update: Update, context: CallbackContext):
    logger.info("Introduction")
    update.message.reply_text(
        'Hello!🎉\nThis bot will help you to find a particular person.',
        reply_markup=reply_markup_help(),
    )
    update.message.reply_text(
        'Enter /start to fill in form',
    )


# Обработчики ConversationHandler
def start_handler(update: Update, context: CallbackContext):
    logger.info('Start search')
    update.message.reply_text(
        '👤Enter name for search. For example, John Smith',
        reply_markup=reply_markup_know(),
    )
    return Q


# Имя
def q_handler(update: Update, context: CallbackContext):
    context.user_data[Q] = update.message.text
    if context.user_data[Q] == "/cancel":
        return cancel_handler(update, context)
    logger.info(f'Name: {context.user_data[Q]}')
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BUTTON_SEX[0]),
                KeyboardButton(text=BUTTON_SEX[1]),
                KeyboardButton(text=BUTTON_SEX[2]),
            ],
        ],
        resize_keyboard=True
    )
    update.message.reply_text(
        '🚹🚺Enter sex of this person.',
        reply_markup=reply_markup,
    )
    return SEX


# Пол
def sex_handler(update: Update, context: CallbackContext):
    context.user_data[SEX] = update.message.text
    if context.user_data[SEX] == "/cancel":
        return cancel_handler(update, context)
    # Замена значений кнопок на значения для запроса к VK
    # Например, man -> 2
    context.user_data[SEX] = replacing_sex(context.user_data[SEX])
    # Валидация
    context.user_data[SEX] = validator(context.user_data[SEX], 0, 2)
    if context.user_data[SEX] is None:
        update.message.reply_text(
            'You entered wrong value. PLease, repeat.',
        )
        return SEX
    logger.info(f'Sex: {context.user_data[SEX]}')
    update.message.reply_text(
        '🏙Enter city.',
        reply_markup=reply_markup_know()
    )
    return CITY


# Город
def city_handler(update: Update, context: CallbackContext):
    context.user_data[CITY] = update.message.text
    if context.user_data[CITY] == "/cancel":
        return cancel_handler(update, context)
    logger.info(f'City: {context.user_data[CITY]}')
    update.message.reply_text(
        '1️⃣Enter age from(> 0).',
        reply_markup=reply_markup_know()
    )
    return AGE_FROM


# Мин. возраст
def age_from_handler(update: Update, context: CallbackContext):
    context.user_data[AGE_FROM] = update.message.text
    if context.user_data[AGE_FROM] == "/cancel":
        return cancel_handler(update, context)
    context.user_data[AGE_FROM] = validator(context.user_data[AGE_FROM], 1, 100)
    if not (context.user_data[AGE_FROM]):
        update.message.reply_text(
            'You entered wrong value. PLease, repeat.',
        )
        return AGE_FROM
    logger.info(f'Age from: {context.user_data[AGE_FROM]}')
    update.message.reply_text(
        '1️⃣0️⃣0️⃣Enter age to( <= 100).',
        reply_markup=reply_markup_know()
    )
    return AGE_TO


# Макс. возраст
def age_to_handler(update: Update, context: CallbackContext):
    context.user_data[AGE_TO] = update.message.text
    if context.user_data[AGE_TO] == "/cancel":
        return cancel_handler(update, context)
    context.user_data[AGE_TO] = validator(context.user_data[AGE_TO], 1, 100)
    # Проверка на то, чтобы мин. возраст не был больше макс. возраста
    if (not (context.user_data[AGE_TO])) or (context.user_data[AGE_FROM] > context.user_data[AGE_TO]):
        update.message.reply_text(
            'You entered wrong value. PLease, repeat.',
        )
        return AGE_TO
    logger.info(f'Age to: {context.user_data[AGE_TO]}')
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_STATUS[0]),
             KeyboardButton(text=BUTTON_STATUS[1]),
             KeyboardButton(text=BUTTON_STATUS[2]),
             KeyboardButton(text=BUTTON_STATUS[3]),
             ],
            [KeyboardButton(text=BUTTON_STATUS[4]),
             KeyboardButton(text=BUTTON_STATUS[5]),
             KeyboardButton(text=BUTTON_STATUS[6]),
             KeyboardButton(text=BUTTON_STATUS[7]),
             ],
            [
                KeyboardButton(text=button_know),
            ]
        ],
        resize_keyboard=True
    )
    update.message.reply_text(
        '💚Enter status.',
        reply_markup=reply_markup,
    )
    return STATUS


# Семейное положение
def status_handler(update: Update, context: CallbackContext):
    context.user_data[STATUS] = update.message.text
    if context.user_data[STATUS] == "/cancel":
        return cancel_handler(update, context)
    context.user_data[STATUS] = replacing_status(context.user_data[STATUS])
    context.user_data[STATUS] = validator(context.user_data[STATUS], 1, 8)
    if not (context.user_data[STATUS]):
        update.message.reply_text(
            'You entered wrong value. PLease, repeat.',
        )
        return STATUS
    logger.info(f'Status: {context.user_data[STATUS]}')
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=1),
             KeyboardButton(text=5),
             KeyboardButton(text=10),
             KeyboardButton(text=15),
             ],
            [
                KeyboardButton(text=button_know),
            ]
        ],
        resize_keyboard=True
    )
    update.message.reply_text(
        '👨‍👩‍👧‍👦Enter the number of users to return.',
        reply_markup=reply_markup,
    )
    return COUNT


def finish_handler(update: Update, context: CallbackContext):
    context.user_data[COUNT] = update.message.text
    if context.user_data[COUNT] == "/cancel":
        return cancel_handler(update, context)
    context.user_data[COUNT] = validator(context.user_data[COUNT], 1, 15)
    logger.info(f'Count: {context.user_data[COUNT]}')
    update.message.reply_text(
        'Result:',
        reply_markup=reply_markup_help(),
    )
    answer = 1
    # Запрос через API ВКонтакте
    response = vk_request(context)
    logger.info(f'Status code:{response.status_code}')
    if response.json().get('response'):
        logger.info(response.json()['response']['items'])
        if not response.json()['response']['items']:
            answer = 0
    if response.json().get('error'):
        logger.info(response.json()['error'])
        answer = 0
    # Вывод результата запроса в сообщениях в Telegram
    if response.status_code == 200 and answer:
        for i in response.json()['response']['items']:
            if not (i.setdefault("city")):
                i["city"] = {}
                i["city"]["title"] = "unspecified"
            if not (i.setdefault("bdate")):
                i["bdate"] = "unspecified"
            update.message.reply_text(
                f'<a href="https://vk.com/id{i["id"]}">&#8205;</a>'
                f'id: {i["id"]}\nfirst name: {i["first_name"]}\nlast name: {i["last_name"]}\n'
                f'city: {i["city"]["title"]}\nbirthday date: {i["bdate"]}\n'
                f'is closed: {i["is_closed"]}\ncan '
                f'access closed: {i["can_access_closed"]}\n',
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            )
    else:
        update.message.reply_text(
            "The request resulted in an error or nothing was found for your request",
        )
    logger.info('Finish search')
    return ConversationHandler.END


# Обработчик команды /cancel - выход из поиска(ConversationHandler)
def cancel_handler(update: Update, context: CallbackContext):
    logger.info('Cancel search')
    update.message.reply_text('Cancel. To start over, enter /start',
                              reply_markup=reply_markup_help(), )
    return ConversationHandler.END


def main():
    logger.info("Launch chat bot")
    # Настройка бота
    req = Request(
        connect_timeout=0.5,
    )
    bot = Bot(
        token=TB_TOKEN,
        request=req,
        # Обход блокировки телеграмм
        # base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True
    )

    handler = ConversationHandler(
        # Точка входа
        entry_points=[
            CommandHandler('start', start_handler),
        ],
        # Словарь состояний
        states={
            Q: [
                MessageHandler(Filters.all, q_handler, pass_user_data=True),
            ],
            SEX: [
                MessageHandler(Filters.all, sex_handler, pass_user_data=True),
            ],
            CITY: [
                MessageHandler(Filters.all, city_handler, pass_user_data=True),
            ],
            AGE_FROM: [
                MessageHandler(Filters.all, age_from_handler, pass_user_data=True),
            ],
            AGE_TO: [
                MessageHandler(Filters.all, age_to_handler, pass_user_data=True),
            ],
            STATUS: [
                MessageHandler(Filters.all, status_handler, pass_user_data=True),
            ],
            COUNT: [
                MessageHandler(Filters.all, finish_handler, pass_user_data=True),
            ],
        },
        fallbacks=[],
    )
    updater.dispatcher.add_handler(handler)
    updater.dispatcher.add_handler(CommandHandler('help', command_help))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo_handler))
    # Проверка, что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')
    updater.start_polling()
    updater.idle()
    logger.info("Shutting down the chatbot")


if __name__ == '__main__':
    main()
