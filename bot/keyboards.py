from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_keyboard(rows: list[list[str]], resize: bool = True) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in rows],
        resize_keyboard=resize,
    )


def main_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    rows = [["Bo'sh ish o'rinlari"]]
    if is_admin:
        rows.append(["📥 Excel yuklash"])
    return make_keyboard(rows)


def departments_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Sotuv bo'limi"],
        ["O'quv ishlari bo'limi"],
        ["Marketing bo'limi"],
        ["⬅️ Orqaga"],
    ])


def sales_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Call Operator"],
        ["Testolog"],
        ["Manager"],
        ["⬅️ Orqaga"],
    ])


def study_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Tillar"],
        ["Fanlar"],
        ["Kasblar"],
        ["⬅️ Orqaga"],
    ])


def languages_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Ingliz tili", "Rus tili"],
        ["Arab tili", "Koreys tili"],
        ["Xitoy tili", "Turk tili"],
        ["⬅️ Orqaga"],
    ])


def subjects_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Ona tili adabiyot", "Tarix"],
        ["Huquq", "Kimyo"],
        ["Biologiya", "Matematika"],
        ["Fizika", "Geografiya"],
        ["⬅️ Orqaga"],
    ])


def professions_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["IT", "Kampyuter"],
        ["Hamshiralik", "Bolalar masaji"],
        ["⬅️ Orqaga"],
    ])


def marketing_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Mobilograf", "Grafik dizayner"],
        ["Print", "Tashqi marketing"],
        ["⬅️ Orqaga"],
    ])


def certificate_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["Bor", "Yo'q"],
        ["⬅️ Bekor qilish"],
    ])


def branches_menu() -> ReplyKeyboardMarkup:
    return make_keyboard([
        ["1️⃣ Niyozbosh"],
        ["2️⃣ Xalqabod"],
        ["3️⃣ Gulbahor"],
        ["4️⃣ Kasblar"],
        ["5️⃣ Kids1"],
        ["6️⃣ Kids2"],
        ["7️⃣ Do'stobod"],
        ["8️⃣ Olmazor"],
        ["9️⃣ Chinoz"],
        ["🔟 Krasin"],
        ["1️⃣1️⃣ Pitiletka"],
        ["1️⃣2️⃣ Qo'rg'oncha"],
        ["1️⃣3️⃣ Kids 3"],
        ["⬅️ Bekor qilish"],
    ])
