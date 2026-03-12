from datetime import datetime
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove

from .config import config
from .excel_utils import append_application, ensure_workbook
from .keyboards import (
    branches_menu,
    certificate_menu,
    departments_menu,
    languages_menu,
    main_menu,
    marketing_menu,
    professions_menu,
    sales_menu,
    study_menu,
    subjects_menu,
)
from .states import VacancyForm

router = Router()

SALES = {"Call Operator", "Testolog", "Manager"}
LANGUAGES = {"Ingliz tili", "Rus tili", "Arab tili", "Koreys tili", "Xitoy tili", "Turk tili"}
SUBJECTS = {"Ona tili adabiyot", "Tarix", "Huquq", "Kimyo", "Biologiya", "Matematika", "Fizika", "Geografiya"}
PROFESSIONS = {"IT", "Kampyuter", "Hamshiralik", "Bolalar masaji"}
MARKETING = {"Mobilograf", "Grafik dizayner", "Print", "Tashqi marketing"}
BRANCHES = {
    "1️⃣ Niyozbosh": "Niyozbosh",
    "2️⃣ Xalqabod": "Xalqabod",
    "3️⃣ Gulbahor": "Gulbahor",
    "4️⃣ Kasblar": "Kasblar",
    "5️⃣ Kids1": "Kids1",
    "6️⃣ Kids2": "Kids2",
    "7️⃣ Do'stobod": "Do'stobod",
    "8️⃣ Olmazor": "Olmazor",
    "9️⃣ Chinoz": "Chinoz",
    "🔟 Krasin": "Krasin",
    "1️⃣1️⃣ Pitiletka": "Pitiletka",
    "1️⃣2️⃣ Qo'rg'oncha": "Qo'rg'oncha",
    "1️⃣3️⃣ Kids 3": "Kids 3",
}
BACK_BUTTONS = {"⬅️ Orqaga", "⬅️ Bekor qilish"}
ADMIN_EXCEL_BUTTON = "📥 Excel yuklash"


def is_admin(user_id: int | None) -> bool:
    return bool(user_id and config.admin_chat_id and user_id == config.admin_chat_id)


def user_main_menu(message: Message):
    return main_menu(is_admin=is_admin(message.from_user.id if message.from_user else None))


def phone_is_valid(text: str) -> bool:
    allowed = set("+0123456789 ")
    return all(ch in allowed for ch in text) and sum(ch.isdigit() for ch in text) >= 9


async def reset_to_main(message: Message, state: FSMContext, text: str = "Asosiy menyu"):
    await state.clear()
    await message.answer(text, reply_markup=user_main_menu(message))


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    ensure_workbook(config.excel_file)
    await state.clear()
    await message.answer(
        "Assalomu alaykum. Vakansiyalar botiga xush kelibsiz. Kerakli bo'limni tanlang.",
        reply_markup=user_main_menu(message),
    )


@router.message(F.text == ADMIN_EXCEL_BUTTON)
async def download_excel_handler(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id if message.from_user else None):
        await message.answer("Bu tugma faqat admin uchun.", reply_markup=user_main_menu(message))
        return

    ensure_workbook(config.excel_file)
    excel_path = Path(config.excel_file)
    if not excel_path.exists():
        await message.answer("Excel fayl topilmadi.", reply_markup=user_main_menu(message))
        return

    await state.clear()
    await message.answer_document(
        FSInputFile(excel_path),
        caption="Excel fayl tayyor.",
        reply_markup=user_main_menu(message),
    )


@router.message(F.text == "Bo'sh ish o'rinlari")
async def vacancies_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bo'limni tanlang:", reply_markup=departments_menu())


@router.message(F.text == "Sotuv bo'limi")
async def sales_handler(message: Message):
    await message.answer("Sotuv bo'limidan lavozimni tanlang:", reply_markup=sales_menu())


@router.message(F.text == "O'quv ishlari bo'limi")
async def study_handler(message: Message):
    await message.answer("Kerakli yo'nalishni tanlang:", reply_markup=study_menu())


@router.message(F.text == "Marketing bo'limi")
async def marketing_handler(message: Message):
    await message.answer("Marketing bo'limidan yo'nalishni tanlang:", reply_markup=marketing_menu())


@router.message(F.text == "Tillar")
async def langs_handler(message: Message):
    await message.answer("Til yo'nalishini tanlang:", reply_markup=languages_menu())


@router.message(F.text == "Fanlar")
async def subj_handler(message: Message):
    await message.answer("Fan yo'nalishini tanlang:", reply_markup=subjects_menu())


@router.message(F.text == "Kasblar")
async def prof_handler(message: Message):
    await message.answer("Kasb yo'nalishini tanlang:", reply_markup=professions_menu())


@router.message(F.text == "⬅️ Orqaga")
async def go_back(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await reset_to_main(message, state, "Ariza bekor qilindi. Asosiy menyuga qaytdingiz.")
        return
    await message.answer("Bo'limni tanlang:", reply_markup=departments_menu())


@router.message(F.text.in_(SALES | LANGUAGES | SUBJECTS | PROFESSIONS | MARKETING))
async def vacancy_selected(message: Message, state: FSMContext):
    selected = message.text

    if selected in SALES:
        department = "Sotuv bo'limi"
    elif selected in (LANGUAGES | SUBJECTS | PROFESSIONS):
        department = "O'quv ishlari bo'limi"
    else:
        department = "Marketing bo'limi"

    await state.update_data(department=department, position=selected)
    await state.set_state(VacancyForm.waiting_full_name)
    await message.answer(
        f"Siz tanlagan yo'nalish: {selected}\n\nF.I.Sh kiriting:",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(VacancyForm.waiting_full_name)
async def get_full_name(message: Message, state: FSMContext):
    if message.text in BACK_BUTTONS:
        await reset_to_main(message, state, "Ariza bekor qilindi.")
        return
    await state.update_data(full_name=message.text.strip())
    await state.set_state(VacancyForm.waiting_birth_date)
    await message.answer("Tug'ilgan sanani kiriting. Masalan: 15.08.2001")


@router.message(VacancyForm.waiting_birth_date)
async def get_birth_date(message: Message, state: FSMContext):
    if message.text in BACK_BUTTONS:
        await reset_to_main(message, state, "Ariza bekor qilindi.")
        return
    await state.update_data(birth_date=message.text.strip())
    await state.set_state(VacancyForm.waiting_certificate)
    await message.answer("Sertifikat bormi?", reply_markup=certificate_menu())


@router.message(VacancyForm.waiting_certificate)
async def get_certificate(message: Message, state: FSMContext):
    if message.text in BACK_BUTTONS:
        await reset_to_main(message, state, "Ariza bekor qilindi.")
        return
    if message.text not in {"Bor", "Yo'q"}:
        await message.answer("Iltimos, faqat 'Bor' yoki 'Yo'q' tugmasini tanlang.", reply_markup=certificate_menu())
        return
    await state.update_data(certificate=message.text)
    await state.set_state(VacancyForm.waiting_phone)
    await message.answer("Telefon raqamingizni kiriting. Masalan: +998901234567", reply_markup=ReplyKeyboardRemove())


@router.message(VacancyForm.waiting_phone)
async def get_phone(message: Message, state: FSMContext):
    if message.text in BACK_BUTTONS:
        await reset_to_main(message, state, "Ariza bekor qilindi.")
        return
    if not phone_is_valid(message.text.strip()):
        await message.answer("Telefon raqam noto'g'ri ko'rinyapti. Masalan: +998901234567")
        return
    await state.update_data(phone=message.text.strip())
    await state.set_state(VacancyForm.waiting_branch)
    await message.answer(
        "Qaysi filialda ishlamoqchisiz?\n\n🏢 Filiallarimiz:",
        reply_markup=branches_menu(),
    )


@router.message(VacancyForm.waiting_branch)
async def get_branch(message: Message, state: FSMContext):
    if message.text in BACK_BUTTONS:
        await reset_to_main(message, state, "Ariza bekor qilindi.")
        return
    if message.text not in BRANCHES:
        await message.answer(
            "Iltimos, filialni tugmalardan tanlang.",
            reply_markup=branches_menu(),
        )
        return
    await state.update_data(branch=BRANCHES[message.text])
    await state.set_state(VacancyForm.waiting_telegram_username)
    await message.answer("Telegram username kiriting. Masalan: @username yoki username", reply_markup=ReplyKeyboardRemove())


@router.message(VacancyForm.waiting_telegram_username)
async def get_username_and_save(message: Message, state: FSMContext):
    if message.text in BACK_BUTTONS:
        await reset_to_main(message, state, "Ariza bekor qilindi.")
        return

    data = await state.get_data()
    candidate_username = message.text.strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        timestamp,
        candidate_username,
        data.get("full_name", ""),
        data.get("birth_date", ""),
        data.get("certificate", ""),
        data.get("phone", ""),
        data.get("branch", ""),
        data.get("department", ""),
        data.get("position", ""),
    ]
    append_application(config.excel_file, row)

    summary = (
        "✅ Arizangiz qabul qilindi.\n\n"
        f"Bo'lim: {data.get('department')}\n"
        f"Lavozim: {data.get('position')}\n"
        f"F.I.Sh: {data.get('full_name')}\n"
        f"Tug'ilgan sana: {data.get('birth_date')}\n"
        f"Sertifikat: {data.get('certificate')}\n"
        f"Telefon: {data.get('phone')}\n"
        f"Filial: {data.get('branch')}\n"
        f"Telegram username: {candidate_username}"
    )
    await message.answer(summary, reply_markup=user_main_menu(message))

    if config.admin_chat_id:
        admin_text = (
            "📥 Yangi vakansiya arizasi\n\n"
            f"Bo'lim: {data.get('department')}\n"
            f"Lavozim: {data.get('position')}\n"
            f"F.I.Sh: {data.get('full_name')}\n"
            f"Tug'ilgan sana: {data.get('birth_date')}\n"
            f"Sertifikat: {data.get('certificate')}\n"
            f"Telefon: {data.get('phone')}\n"
            f"Filial: {data.get('branch')}\n"
            f"Telegram username: {candidate_username}"
        )
        await message.bot.send_message(config.admin_chat_id, admin_text)

    await state.clear()


@router.message()
async def fallback_handler(message: Message):
    await message.answer("Kerakli tugmani tanlang yoki /start bosing.", reply_markup=user_main_menu(message))
