from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    add_name = State()
    add_coord = State()
    add_text = State()
    add_photo = State()
    add_link = State()
    menu = State()
    show = State()
    sent = State()
