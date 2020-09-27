from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    add_name = State()
    add_hyperlinks = State()
    add_text = State()
    add_photo = State()
    add_link = State()
    add_schedule = State()
    menu = State()
    show = State()
    sent = State()
    select_in_schedule = State()
    edit_time = State()
