from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def tone_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎉 Весёлый", callback_data="tone_fun")],
        [InlineKeyboardButton(text="❤️ Трогательный", callback_data="tone_warm")],
        [InlineKeyboardButton(text="🎩 Официальный", callback_data="tone_formal")],
        [InlineKeyboardButton(text="✨ Творческий", callback_data="tone_creative")],
    ])


def length_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Короткое (6-8 предложений) — 249 ₽", callback_data="length_short")],
        [InlineKeyboardButton(text="📃 Среднее (12-16 предложений) — 349 ₽", callback_data="length_medium")],
        [InlineKeyboardButton(text="📜 Длинное (18-24 предложения) — 449 ₽", callback_data="length_long")],
    ])


def delivery_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Показать в Telegram", callback_data="delivery_telegram")],
        [InlineKeyboardButton(text="📧 Отправить на e-mail", callback_data="delivery_email")],
    ])


def variant_choice_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать вариант 1", callback_data="choose_variant_1")],
        [InlineKeyboardButton(text="Выбрать вариант 2", callback_data="choose_variant_2")],
    ])


    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SHARE_TEXT = (
    "🎉 Нашёл классного бота для поздравлений!\n\n"
    "Он создаёт уникальные тёплые поздравления с помощью ИИ — "
    "быстро, красиво и с душой ❤️\n\n"
    "Попробуй сам — жми и создавай свои поздравления 👇\n"
    "@pozdravlyashka2026_bot"
)

def get_share_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📤 Поделиться с другом",
            switch_inline_query=SHARE_TEXT
        )]
    ])
    return keyboard