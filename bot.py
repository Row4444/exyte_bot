import logging
import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.webhook import SendPhoto
from aiogram.types import InputMediaPhoto

from controller import get_currency_today, get_graph_costs_per_week

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await message.answer("Hi. It's test work.\n"
                         "Click /help to see more.")


@dp.message_handler(commands=['help'])
async def send_help(message):
    await message.answer("Commands list:\n"
                         "Use\n"
                         "/lst or /list\n"
                         "to see all for today;\n"
                         "\n"
                         "Use\n"
                         "/history <your currency>\n"
                         "or\n"
                         "/<your currency> for <count> days\n"
                         "to see history of Currency.\n")


def get_symbol(message):
    """ Берет из сообщения валюту и коли-во дней(если есть) и возвращает их"""
    message_array = message.text.split()
    if message_array[0] == '/history' \
            and len(message_array) == 2:
        return (message_array[1].upper(),) \
            if len(message_array[1]) == 3 else False
    elif len(message_array) == 4 \
            and message_array[1].lower() == 'for' \
            and message_array[3].lower() == 'days':
        try:
            message_array[2] = int(message_array[2])
        except ValueError:
            return False
        return message_array[0][1:].upper(), message_array[2]
    else:
        return False


@dp.message_handler(commands=['list', 'lst'])
async def send_currency_list(message):
    """ Отдает список всех валют """
    answer = get_currency_today()
    if answer:
        await message.answer(answer)
    else:
        await error_message(message)


@dp.message_handler(lambda message: (message.text[0] == "/" and len(message.text.split()) == 4)
                                    or message.text.startswith('/history'))
async def send_history(message):
    """ Отправляет графф с историей """
    symbol = get_symbol(message)
    if not symbol:
        await error_message(message)
    else:
        graph = get_graph_costs_per_week(*symbol)
        if graph:
            await bot.send_photo(chat_id=message.from_user.id, photo=open(graph, 'rb'))
        else:
            await message.answer("No exchange rate data is available for the selected currency.")


@dp.message_handler()
async def error_message(message):
    """ Сообщение об неверном запросе """
    await message.answer("Sorry. I don't understand."
                         "See /help to know what i can do.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
