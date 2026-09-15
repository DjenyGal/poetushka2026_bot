from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    q_name = State()
    q_age = State()
    q_relationship = State()
    q_occasion = State()
    q_tone = State()
    q_length = State()
    q_details = State()
    q_secrets = State()
    q_signature = State()
    q_delivery = State()
    q_email = State()
    choosing_variant = State()