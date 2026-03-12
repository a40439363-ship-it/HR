# Vakansiyalar Telegram bot

Bu bot vakansiya uchun ariza yig'adi va barcha arizalarni Excel faylga yozadi. Har bir yangi ariza admin chatga ham yuboriladi.

## Imkoniyatlar
- Bo'sh ish o'rinlari menyusi
- Sotuv, O'quv ishlari, Marketing bo'limlari
- Filial tanlash
- Admin uchun **📥 Excel yuklash** tugmasi
- Excel fayl avtomatik yaratiladi

## Railway uchun tayyorlangan
- `.env` project ichidan olib tashlangan
- `Procfile` qo'shilgan
- `runtime.txt` qo'shilgan
- `railway.json` qo'shilgan
- Excel yo'li Railway volume bo'lsa avtomatik moslashadi

## Local ishga tushirish
```bash
pip install -r requirements.txt
python main.py
```

## Railway Variables
Railway > Project > Variables ichiga quyidagilarni qo'ying:

- `BOT_TOKEN` = Telegram bot token
- `ADMIN_CHAT_ID` = admin Telegram ID

Ixtiyoriy:
- `EXCEL_FILE` = to'liq excel yo'li
- yoki `DATA_DIR` = papka yo'li, masalan `/data`

## Railway Start Command
Agar kerak bo'lsa, start command:
```bash
python main.py
```

## Muhim eslatma
Agar Railway volume ulamasangiz, Excel fayl restartdan keyin saqlanmay qolishi mumkin. Eng yaxshi variant: Railway volume ulash yoki keyinchalik PostgreSQL ga o'tish.
