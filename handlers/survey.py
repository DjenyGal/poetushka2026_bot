from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.order_states import OrderStates
from keyboards.inline import tone_keyboard, length_keyboard
from database.requests import create_order, update_order
from config import PRICES

router = Router()


@router.message(OrderStates.q_name)
async def process_name(message: Message, state: FSMContext):
    order_id = await create_order(message.from_user.id)
    await update_order(order_id, name=message.text)
    await state.update_data(order_id=order_id)

    await state.set_state(OrderStates.q_age)
    await message.answer("Можно узнать возраст виновника торжества?")


@router.message(OrderStates.q_age)
async def process_age(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], age=message.text)

    await state.set_state(OrderStates.q_relationship)
    await message.answer("Кем виновник торжества вам приходится?")


@router.message(OrderStates.q_relationship)
async def process_relationship(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], relationship=message.text)

    await state.set_state(OrderStates.q_occasion)
    await message.answer("Какой повод: что празднуем?")


@router.message(OrderStates.q_occasion)
async def process_occasion(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], occasion=message.text)

    await state.set_state(OrderStates.q_tone)
    await message.answer("Степень «градуса»: какой стиль выбираем?", reply_markup=tone_keyboard())


@router.callback_query(OrderStates.q_tone, F.data.startswith("tone_"))
async def process_tone(callback: CallbackQuery, state: FSMContext):
    tone = callback.data.split("tone_")[1]
    data = await state.get_data()
    await update_order(data["order_id"], tone=tone)

    await state.set_state(OrderStates.q_length)
    await callback.message.edit_text("Тон выбран ✅")
    await callback.message.answer(
        "Какой объём текста нужен?",
        reply_markup=length_keyboard()
    )


@router.callback_query(OrderStates.q_length, F.data.startswith("length_"))
async def process_length(callback: CallbackQuery, state: FSMContext):
    length = callback.data.split("length_")[1]
    price = PRICES[length]

    data = await state.get_data()
    await update_order(data["order_id"], length=length, price=price)

    await state.set_state(OrderStates.q_details)
    await callback.message.edit_text(f"Объём выбран ✅ Стоимость: {price} ₽")
    await callback.message.answer(
        "Щепотка его профессии и стакан хобби\n\n"
        "Например: «работает врачом», «обожает путешествия», «недавно переехал в новую квартиру»\n\n"
        "Если нет — напишите «нет»"
    )


@router.message(OrderStates.q_details)
async def process_details(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], details=message.text)

    await state.set_state(OrderStates.q_secrets)
    await message.answer(
        "Скелеты в шкафу (индивидуальные детали)\n\n"
        "Чем больше жирного компромата и фактов вы сольете, тем сильнее будет разрыв шаблона. Есть ли у человека странные привычки, коронные фразы, провальные истории или достижения, которыми стоит похвастаться? Чем больше «грязного белья» (в хорошем смысле), тем круче будет текст.\n\n"
        "Если нет — напишите «нет»"
    )


@router.message(OrderStates.q_secrets)
async def process_secrets(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_order(data["order_id"], secrets=message.text)

    await state.set_state(OrderStates.q_signature)
    await message.answer(
        "Как подписать сей шедевр?\n\n"
        "Например: «Твоя сестра Оля», «Коллеги из отдела продаж», «С любовью, Саша»"
    )

@router.message(OrderStates.q_signature)
async def process_signature(message: Message, state: FSMContext):
    from keyboards.inline import delivery_keyboard

    data = await state.get_data()
    await update_order(data["order_id"], signature=message.text)

    await state.set_state(OrderStates.q_delivery)
    await message.answer(
        "Как хотите получить готовое поздравление?",
        reply_markup=delivery_keyboard()
    ) 