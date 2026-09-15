from config import LENGTH_LABELS
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from states.order_states import OrderStates
from keyboards.inline import variant_choice_keyboard
from keyboards.reply import restart_keyboard
from database.requests import update_order, get_order
from services.ai_service import generate_greeting

router = Router()


SHARE_TEXT = (
    "🎉 Нашёл классного бота для поздравлений!\n\n"
    "Он создаёт уникальные тёплые поздравления с помощью ИИ — "
    "быстро, красиво и с душой ❤️\n\n"
    "Попробуй сам 👇\n"
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


def make_preview(text: str, sentences_count: int = 2) -> str:
    parts = text.replace("\n", " ").split(". ")
    preview = ". ".join(parts[:sentences_count])
    if not preview.endswith("."):
        preview += "."
    return preview + "\n\n[... полный текст откроется после оплаты]"


@router.callback_query(OrderStates.q_delivery, F.data == "delivery_telegram")
async def delivery_telegram(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], delivery_method="telegram")

    await callback.message.edit_text("Способ доставки: Telegram ✅")
    await start_generation(callback.message, state)


@router.callback_query(OrderStates.q_delivery, F.data == "delivery_email")
async def delivery_email(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStates.q_email)
    await callback.message.edit_text("Способ доставки: E-mail ✅")
    await callback.message.answer("Напишите, пожалуйста, вашу почту:")


@router.message(OrderStates.q_email)
async def process_email(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], delivery_method="email", email=message.text)

    await start_generation(message, state)


async def start_generation(message: Message, state: FSMContext):
    data = await state.get_data()
    order = await get_order(data["order_id"])

    wait_msg = await message.answer("✨ Генерирую поздравление, это займёт около 15-20 секунд...")

    order_data = {
        "name": order.name,
        "age": order.age,
        "relationship": order.relationship,
        "occasion": order.occasion,
        "tone": order.tone,
        "length": order.length,
        "details": order.details,
        "secrets": order.secrets,
        "signature": order.signature,
    }

    variants = await generate_greeting(order_data)

    await update_order(data["order_id"], variant_1=variants[0], variant_2=variants[1])
    await state.update_data(variant_1=variants[0], variant_2=variants[1])

    await wait_msg.delete()

    preview_1 = make_preview(variants[0])
    preview_2 = make_preview(variants[1])

    await message.answer(
        f"Готово! Вот два варианта поздравления (черновик для выбора):\n\n"
        f"📝 <b>Вариант 1:</b>\n{preview_1}\n\n"
        f"📝 <b>Вариант 2:</b>\n{preview_2}\n\n"
        f"Выберите понравившийся вариант, полный текст откроется после оплаты 👇",
        parse_mode="HTML",
        reply_markup=variant_choice_keyboard()
    )

    await state.set_state(OrderStates.choosing_variant)


@router.callback_query(OrderStates.choosing_variant, F.data.startswith("choose_variant_"))
async def choose_variant(callback: CallbackQuery, state: FSMContext):
    variant_num = callback.data.split("choose_variant_")[1]
    data = await state.get_data()

    chosen_text = data["variant_1"] if variant_num == "1" else data["variant_2"]

    await update_order(data["order_id"], chosen_variant=variant_num)
    await state.update_data(chosen_text=chosen_text)

    await callback.message.edit_text(f"Вы выбрали вариант {variant_num} ✅")

    # Здесь дальше будет переход к оплате
    await callback.message.answer(
        "Отлично! Переходим к оплате...\n\n"
        "(здесь будет логика оплаты — обсудим отдельно)",
        reply_markup=restart_keyboard()
    )

    await callback.message.answer(
        "А если хочешь порадовать друга — поделись ботом с ним 👇",
        reply_markup=get_share_keyboard()
    )