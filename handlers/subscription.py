from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import CHANNEL_ID, CHANNEL_LINK
from states.order_states import OrderStates
from keyboards.reply import start_keyboard

router = Router()


async def is_subscribed(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    subscribed = await is_subscribed(message.bot, message.from_user.id)

    if not subscribed:
        await message.answer(
            f"Привет, {message.from_user.first_name}! 👋\n\n"
            f"Чтобы пользоваться ботом, подпишись на наш канал: {CHANNEL_LINK}\n\n"
            f"После подписки нажми на кнопку ниже.",
        )
        await message.answer(
            "Итак, начинаем",
            reply_markup=start_keyboard()
        )
        return

    await message.answer(
        f"Отлично, {message.from_user.first_name}, вы подписаны! ✅",
        reply_markup=start_keyboard()
    )


@router.message(F.text == "Итак, начинаем")
async def start_survey(message: Message, state: FSMContext):
    subscribed = await is_subscribed(message.bot, message.from_user.id)

    if not subscribed:
        await message.answer(
            f"Похоже, вы ещё не подписались на канал, там вы найдете много интересного для себя: {CHANNEL_LINK}\n\n"
            f"Подпишитесь и нажмите кнопку ещё раз."
        )
        return

    await message.answer(
        "Отлично! Я — Поздравляшка — доверьте магию слов мне! 📜 Чтобы поздравление получилось по-настоящему личным и живым, мне нужны ваши подсказки. "
        "Заполните небольшую анкету ниже: укажите повод, поделитесь фактами о человеке и выберите настроение текста. Всего пара минут — и идеальная проза готова! 🎉\n\n"
        "Как зовут счастливчика или жертву?"
    )
    await state.set_state(OrderStates.q_name)


@router.message(F.text == "Начать сначала")
async def restart_survey(message: Message, state: FSMContext):
    await start_survey(message, state)


@router.message(F.text == "Поделиться с друзьями")
async def share_with_friends(message: Message):
    bot_info = await message.bot.get_me()
    bot_username = bot_info.username

    share_text = (
        f"🎉 Хочешь крутое поздравление за пару минут?\n\n"
        f"Бот Поздравляшка — напишет уникальное поздравление специально для Вас!\n\n"
        f"👉 https://t.me/pozdravlyashka2026_bot"
    )

    await message.answer(
        f"Вот текст, которым можно поделиться с друзьями:\n\n{share_text}"
    )