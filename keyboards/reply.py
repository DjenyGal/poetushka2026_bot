from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Итак, начинаем")]],
        resize_keyboard=True,
        is_persistent=True
    )


def restart_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Начать сначала")],
            [KeyboardButton(text="Поделиться с друзьями")]
        ],
        resize_keyboard=True,
        is_persistent=True
    )