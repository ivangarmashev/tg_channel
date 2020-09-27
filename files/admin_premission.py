from aiogram import types
from aiogram.dispatcher import FSMContext
from files.connections import dp
from files import keyboards as kb
password = 'f4fbe2e031322d3039d5da3334e0f4fbef' \
        '32c0c94141ebe5eaf1e5e5e2e0f4fbf4fb' \
        'e2ef33e2e031322234332f2d2aeafc6669' \
        '6a6f6173313233347d5f5f7c3c4d4d3233' \
        '34c0c235363132332b2a2d313440353139' \
        '39393531233233346c7361646631363431' \
        '323333313231326673616640292821232d' \
        '2f2affcbf7ebe6eff03134'


@dp.message_handler(text=password, content_types=types.ContentTypes.TEXT)
async def menu_schedule(message: types.Message, state: FSMContext):
    await state.set_state('States:menu')
    await message.answer_sticker(sticker='CAACAgIAAxkBAAIeLl9wlhFm67OkEo'
                                         'P7r3CL0xSNIGgcAAI8AAOmbqkdcEYEyiuZjO0bBA',
                                 reply_markup=kb.start)
