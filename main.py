import sqlite3
from random import randint

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import BotCommand, Message

# Создаем объекты бота и диспетчера
bot = Bot(token="ВАШ ТОКЕН")
dp = Dispatcher()


def random_book():
    con = sqlite3.connect('books.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT name FROM book""").fetchall()
    rand = randint(0, len(result) - 1)
    select_book = (result[rand][0])
    book = cur.execute(f"""SELECT * FROM book WHERE name = '{select_book}'""").fetchall()
    con.close()
    return book[0]


def polizovat(id):
    global a
    # flag = False
    flag = False
    con = sqlite3.connect('books.db')
    cur = con.cursor()
    result_id = cur.execute(f"""SELECT user FROM users
    WHERE user = '{id}'""").fetchall()
    if result_id:
        result = cur.execute(f"""SELECT prochitano FROM users
        WHERE user = '{id}'""").fetchone()
    else:
        a = cur.execute(f'''INSERT INTO users(user) VALUES('{id}')''')
        con.commit()
        flag = True
    con.close()
    if flag:
        a = random_book()
        return str(f'{a[2]} "{a[0]}"\n{a[1]}\nПоджанры: {a[3]}\n\n{a[5]}')
    else:
        mama = 0
        while True:
            mama += 1
            a = random_book()
            if result[0] != None:
                book_prochit = [(result[0].split('---'))[i] for i in range(len(result[0].split('---')))]
                if a[0] not in book_prochit:
                    return str(f'{a[2]} "{a[0]}"\n{a[1]}\nПоджанры: {a[3]}\n\n{a[5]}')
                if mama == 50:
                    return str('Вы прочитали все мои книги!!!')
            else:
                return str(f'{a[2]} "{a[0]}"\n{a[1]}\nПоджанры: {a[3]}\n\n{a[5]}')


# ----------------------------------------------------------------------------------------------------------------------
# Создаем объекты кнопок
button_1 = InlineKeyboardButton(
    text='Прочитано🦐',
    callback_data='button_1_pressed'
)

button_2 = InlineKeyboardButton(
    text='Ещё',
    callback_data='button_2_pressed'
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button_1], [button_2]]
)


@dp.message(Command(commands=['start']))
async def process_help_command(message: Message):
    k = polizovat(f'{message.from_user.id}')
    if k == 'Вы прочитали все мои книги!!!':
        await message.answer(
            text=k,
        )
    else:
        await message.answer(
            text=k,
            reply_markup=keyboard
        )


# ----------------------------------------
@dp.callback_query(F.data == 'button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    con = sqlite3.connect('books.db')
    cur = con.cursor()
    znach = cur.execute(f"""SELECT prochitano FROM users
        WHERE user = '{callback.from_user.id}'""").fetchone()
    if znach[0]:
        znach = znach[0] + '---' + a[0]
    else:
        znach = a[0]
    result = cur.execute(f"""UPDATE users
    SET prochitano = '{znach}'
    WHERE user = '{callback.from_user.id}'""").fetchall()
    con.commit()
    con.close()
    await callback.answer(text='Умничка! Больше я не посоветую тебе эту книгу!')


@dp.callback_query(F.data == 'button_2_pressed')
async def process_button_1_press(callback: CallbackQuery):
    await callback.answer(text='Напиши /start')


# -----------------------------------------------------------------------------------------------------------------------
# всё для about

url_button_1 = InlineKeyboardButton(
    text='Тг - канал автора',
    url='https://t.me/+ssL_Dvk2ckplY2Uy'
)

url_button_2 = InlineKeyboardButton(
    text='Инста автора',
    url=f'https://www.instagram.com/fir_fir_kefir?igsh=djdwaW1xbnQ0emZu'
)

keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1],
                     [url_button_2]]
)


@dp.message(Command(commands=['about']))
async def process_help_command(message: Message):
    await message.answer(
        text='Автор просто советует книжки :3',
        reply_markup=keyboard2
    )


# -----------------------------------------------------------------------------------------------------------------------

#  хэндлер на команду "/add_new"
@dp.message(Command(commands=['add_new']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши название\n'
        'Напиши автора\n'
        'Жанры и поджанры\n'
        'Можешь написать сюжет, как ты его видишь\n'
    )


# ----------------------------------------------------------------------------------------
#  хэндлер на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        '/start - чтобы начать \n'
        '/about - информация об авторе\n'
        '/help - основные команды\n'
        '/add_new - предложить добавить книгу'
    )


# ----------------------------------------------------------------------------------------
# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start', description='Начать работу с ботом'),
        BotCommand(command='/help', description='Справка'),
        BotCommand(command='/about', description='Об авторе'),
        BotCommand(command='/add_new', description='Предложение добавить вашу книгу')
    ]
    await bot.set_my_commands(main_menu_commands)


@dp.message()
async def send_answer(message: Message):
    # print(message.text, message.animation, message.photo)
    await message.answer(text='Не знаю такой ответ, попроси книгу через /start')


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
