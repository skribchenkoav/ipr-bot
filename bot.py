from api.api import get_standings, get_fixtures
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import teams
from config import config


TOKEN = config.TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    text = 'Данный бот позволяет узнавать информацию об английской премьер-лиге (АПЛ).\nВведите /help для получения ' \
           'списка команд. '
    await message.answer(text)


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    text = '/standings - турнирная таблица\n/fixtures - список матчей в ближайшую неделю\n/team - узнать информацию о ' \
           'команде\n/cancel - отмена действия'
    await message.answer(text)


@dp.message_handler(commands=['standings'])
async def standings_handler(message: types.Message):
    text = get_standings('PL')
    await message.answer(text)


@dp.message_handler(commands=['fixtures'])
async def fixtures_handler(message: types.Message):
    text = get_fixtures('PL')
    await message.answer(text)


@dp.message_handler(commands=['cancel'], state="*")
@dp.message_handler(filters.Text(equals="отмена", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")

if __name__ == '__main__':
    teams.register_handlers_teams(dp)
    executor.start_polling(dp)


