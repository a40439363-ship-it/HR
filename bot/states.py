from aiogram.fsm.state import State, StatesGroup


class VacancyForm(StatesGroup):
    waiting_full_name = State()
    waiting_birth_date = State()
    waiting_certificate = State()
    waiting_phone = State()
    waiting_branch = State()
    waiting_telegram_username = State()
