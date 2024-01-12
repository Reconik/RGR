import sqlite3
import pandas as pd
import telebot
from telebot import types

bot = telebot.TeleBot("6922281663:AAGxA2tax67K7KcA6vZKim4BAzpJEYdzHko")

df = pd.read_csv('https://raw.githubusercontent.com/Reconik/RGR/main/text.csv')

keyboard = types.InlineKeyboardMarkup(row_width=3)
BPMN_button = types.InlineKeyboardButton('Схема BPMN', callback_data='bpmn')
dashboard_button = types.InlineKeyboardButton('Дашборд', callback_data='dashboard')
suppliers_button = types.InlineKeyboardButton('Список поставщиков', callback_data='suppliers')
order_button = types.InlineKeyboardButton('Оформить заказ', callback_data='order')
find_item_button = types.InlineKeyboardButton('Проверить товар', callback_data='lookforitem')
about_bot_button = types.InlineKeyboardButton('Функции бота', callback_data='about_bot')
keyboard.add(BPMN_button, dashboard_button, suppliers_button, order_button, find_item_button,  about_bot_button)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Я бот по закупке товаров оптом для магазинов. Чем могу помочь?''\n'
                                      'Тут можно создавать запросы на оптовую закупку товаров в магазины')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)


@bot.message_handler(commands=['поставщики'])
def suppliers(message):
    # Здесь можно добавить код для получения информации о поставщиках
    bot.send_message(message.chat.id, 'Список поставщиков: Поставщик 1, Поставщик 2, Поставщик 3')
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# Ответ на запрос о создателе
def About_(message):
    bot.reply_to(message, 'Слободяник С.В. 2ИБ-1')


# кнопки для действий с Дашбордом
def Dashboard_but(message):
    dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
    button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
    dashboard_markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)


# кнопка для оформления заказа
def order_handler(message):
    bot.send_message(message.chat.id, 'Оформление заказа. \n'
                                           f'Введите ваше имя:')
    bot.register_next_step_handler(message, enter_sender_name)

# Ввод имени
def enter_sender_name(message):
    order = {}
    order['sender_name'] = message.text
    bot.send_message(message.chat.id, f'Отлично, {message.text}! Выберите поставщика:')
    bot.register_next_step_handler(message, enter_suppliers, order)

# Обработчик выбора поставщика
def enter_suppliers(message, order):
    order['suppliers'] = message.text
    bot.send_message(message.chat.id, f'Отлично, {message.text}! Выберите товары и количество для приобретения:')
    bot.register_next_step_handler(message, enter_item, order)

# Обработчик для ввода места подачи груза
def enter_item(message, order):
    order['item'] = message.text
    bot.send_message(message.chat.id, f'Поставщик: {message.text}. Введите пункт назначения:')
    bot.register_next_step_handler(message, enter_destination, order)

# Обработчик для ввода пункта назначения
def enter_destination(message, order):
    order['destination'] = message.text
    bot.send_message(message.chat.id, f'Пункт назначения: {message.text}.\n\n' 
                                      f'Заказ успешно оформлен!')

    # отчет о заказе
    report = f'Отчет по заказу:\n\n' \
             f'Имя отправителя: {order["sender_name"]}\n' \
             f'Товары для приобретения и их количество: {order["item"]}\n' \
             f'Выбран поставщик: {order["suppliers"]}\n' \
             f'Пункт назначения: {order["destination"]}\n'

    # Отправка отчета пользователю
    bot.send_message(message.chat.id, report)
    # Создание подключения к базе данных SQLite
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()


def look_for_item(message):
    bot.send_message(message.chat.id, 'Введите название товаров:')
    bot.register_next_step_handler(message, look_for_item_)

def look_for_item_(message):
    me = message
    item_name = message.text
    found = df[df['Товар'] == item_name]
    if (len(found) == 0):
        bot.send_message(me.chat.id, "Нет товаров с таким названием")
    else:
        bot.send_message(me.chat.id, f'Товаров присутствует, всего {len(found)} \n'
                                     'Вот некоторые из найденных:')
        i = 3
        for x in found.index:
            i -= 1
            if i == 0:
                break
            item_date = found['Дата'][x]
            item_sum = found['Сумма'][x]
            bot.send_message(me.chat.id, f'{item_name}, дата {item_date}, стоимость {item_sum} рублей')


def notify_order_status(order_id, status):
    # Здесь можно добавить логику отправки уведомления о состоянии заказа
    bot.send_message(order_id, f'Статус вашего заказа: {status}')

def notify_payment_status(order_id, status):
    # Здесь можно добавить логику отправки уведомления о состоянии оплаты
    bot.send_message(order_id, f'Статус оплаты вашего заказа: {status}')


bpmn_image_url = 'https://github.com/Reconik/RGR/blob/Developed/BPMN-%D1%81%D1%85%D0%B5%D0%BC%D0%B0.PNG?raw=true'
bpmn_but = lambda mes: bot.send_photo(mes.chat.id, bpmn_image_url, caption='BPMN карта')

image1_url = 'https://github.com/Reconik/RGR/blob/main/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D0%BA%20%D1%80%D0%B0%D1%81%D1%81%D0%B5%D1%8F%D0%BD%D0%B8%D1%8F.PNG?raw=true'
image2_url = 'https://github.com/Reconik/RGR/blob/main/%D0%94%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%20%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.PNG?raw=true'
image3_url = 'https://github.com/Reconik/RGR/blob/main/%D0%9A%D1%80%D1%83%D0%B3%D0%BE%D0%B2%D0%BE%D0%B9%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA.PNG?raw=true'
image4_url = 'https://github.com/Reconik/RGR/blob/main/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.PNG?raw=true'

dashboard_2 = lambda mes: bot.send_message(mes.chat.id, 'Ссылка на GitHub: https://github.com/Reconik/Dashboard/tree/Test-dashboard')
dashboard_3 = lambda mes: bot.send_photo(mes.chat.id, image1_url, caption='График рассеивания')
dashboard_4 = lambda mes: bot.send_photo(mes.chat.id, image2_url, caption='Диаграмма анализа данных')
dashboard_5 = lambda mes: bot.send_photo(mes.chat.id, image3_url, caption='Круговой график')
dashboard_6 = lambda mes: bot.send_photo(mes.chat.id, image4_url, caption='Таблица данных')

CALLBACK_D_BUTTON = {
    "bpmn": bpmn_but,
    "dashboard": Dashboard_but,
    "order": order_handler,
    "lookforitem": look_for_item,
    "dashboard_function2": dashboard_2,
    "dashboard_function3": dashboard_3,
    "dashboard_function4": dashboard_4,
    "dashboard_function5": dashboard_5,
    "dashboard_function6": dashboard_6,
}

# Обработчик на нажатие клавиш
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in CALLBACK_D_BUTTON:
        CALLBACK_D_BUTTON[call.data](call.message)
    elif call.data == 'about_bot':
        bot.send_message(call.message.chat.id,
                         'Telegram-бот может значительно упростить и ускорить процесс оптовой закупки'
                         'для магазинов.\n'
                         'Функции которые можно автоматизировать с помощью данного бота:'
                         '\nПрием заказов: Клиенты могут делать заказы через бота, указывая необходимую информацию,'
                         ' такую как место погрузки, пункт назначения, тип груза и выбирать поставщика.'
                         '\nИнтеграция с разными платежными системами: Для удобства клиентов бот может интегрироваться с платежными системами, '
                         'позволяя им платить прямо через Telegram.'
                         '\nОбратная связь: Клиенты могут общаться с ботом, '
                         'чтобы задать вопросы, уточнить детали заказа или оставить отзыв.')
    elif call.data == 'dashboard':
        dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
        button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
        dashboard_markup.add(button1, button2)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)
    elif call.data == 'dashboard_function1':
        bot.send_message(call.message.chat.id, 'Дашборд показывает и информирует пользвователя о наличии, '
                                               'распределении товаров по их категории, дате, количеству и их стоимости. ')
        dashboard_function_markup = types.InlineKeyboardMarkup(row_width=1)
        button3 = types.InlineKeyboardButton('График рассеивания', callback_data='dashboard_function3')
        button4 = types.InlineKeyboardButton('Диаграмма анализа данных', callback_data='dashboard_function4')
        button5 = types.InlineKeyboardButton('Круговой график', callback_data='dashboard_function5')
        button6 = types.InlineKeyboardButton('Таблица данных', callback_data='dashboard_function6')
        dashboard_function_markup.add(button3, button4, button5, button6)
        bot.send_message(call.message.chat.id, 'Выберите график:', reply_markup=dashboard_function_markup)
    elif call.data == 'suppliers':
        bot.send_message(call.message.chat.id, 'Список поставщиков: Поставщик 1, Поставщик 2, Поставщик 3')


if __name__ == "__main__":
    bot.infinity_polling()
