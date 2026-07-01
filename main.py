import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
load_dotenv()
dv
# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

# FSM (Finite State Machine) holatlari
class Registration(StatesGroup):
    waiting_name = State()
    waiting_age = State()

# /start komandasi uchun handler
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Registration.waiting_name)

# Ismni qabul qilish xonasi (faqat waiting_name holatida ishlaydi)
@dp.message(Registration.waiting_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Rahmat, {message.text}! Endi yoshingizni kiriting:")
    await state.set_state(Registration.waiting_age)

# Yoshni qabul qilish xonasi (faqat waiting_age holatida ishlaydi)
@dp.message(Registration.waiting_age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, yoshingizni raqamda kiriting.")
        return
    
    # Ma'lumotlarni olish
    data = await state.get_data()
    name = data.get("name")
    age = message.text
    
    await message.answer(
        f"Ro'yxatdan o'tdingiz!\nIsm: {name}\nYosh: {age}"
    )
    # Holatni tozalash
    await state.clear()

# Botni ishga tushirish funksiyasi
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
