from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from api.api import get_league_teams, get_team


class TeamSelect(StatesGroup):
    printing_team = State()


async def team_start(message: types.Message, state: FSMContext):
    text = get_league_teams('PL')
    await message.answer('Список команд и их ID:')
    await message.answer(text)
    await message.answer('Введите ID команды:')
    await state.set_state(TeamSelect.printing_team.state)


async def team_selected(message: types.Message, state: FSMContext):
    team_id = message.text
    text = get_team(team_id)
    await message.answer(text)
    await state.finish()


def register_handlers_teams(dp: Dispatcher):
    dp.register_message_handler(team_start, commands=['team'], state="*")
    dp.register_message_handler(team_selected, state=TeamSelect.printing_team)
