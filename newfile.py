from datetime import datetime
from telebot import TeleBot, types

# ------------------ تنظیمات اصلی ------------------
BOT_TOKEN ="8520099119:AAF6kSG-JlZ5Ar1gFCt8KbnNxjQ5EHmcoVA"
bot = TeleBot(BOT_TOKEN)
ADMIN_ID = 1474297509

file_customers = {}      # شماره موبایل → تعداد خرید فایل
user_order_step = {}     # chat_id → مرحله سفارش

# ------------------ تاریخ افزایش قیمت ------------------
PRICE_INCREASE_DATE = datetime(2026, 9, 22)  # حدوداً 1 مهر 1405

def get_final_price(base_price: int, is_madadjo: bool, phone: str) -> tuple:
    now = datetime.now()
    if now >= PRICE_INCREASE_DATE:
        base_price = int(base_price * 1.4)

    discount_text = ""
    if is_madadjo:
        final_price = int(base_price * 0.85)
        discount_text = "🎉 تخفیف ۱۵٪ مددجویان اعمال شد.\n"
    elif phone in file_customers:
        final_price = int(base_price * 0.9)
        discount_text = "🎉 تخفیف ۱۰٪ مشتریان فایل اعمال شد.\n"
    else:
        final_price = base_price

    return final_price, discount_text

# ------------------ ساختار پایه‌ها و درس‌ها ------------------
subjects = {
    "ابتدایی": {
        "پایه اول": ["ریاضی", "علوم", "فارسی", "مطالعات", "هدیه‌ها", "نگارش"],
        "پایه دوم": ["ریاضی", "علوم", "فارسی", "مطالعات", "هدیه‌ها", "نگارش"],
        "پایه سوم": ["ریاضی", "علوم", "فارسی", "مطالعات", "هدیه‌ها", "نگارش"],
        "پایه چهارم": ["ریاضی", "علوم", "فارسی", "مطالعات", "هدیه‌ها", "نگارش"],
        "پایه پنجم": ["ریاضی", "علوم", "فارسی", "مطالعات", "هدیه‌ها", "نگارش"],
        "پایه ششم": ["ریاضی", "علوم", "فارسی", "مطالعات", "هدیه‌ها", "نگارش"]
    },
    "راهنمایی": {
        "هفتم": ["ریاضی", "علوم", "فارسی", "مطالعات", "پیام‌های آسمانی", "نگارش", "عربی", "انگلیسی"],
        "هشتم": ["ریاضی", "علوم", "فارسی", "مطالعات", "پیام‌های آسمانی", "نگارش", "عربی", "انگلیسی"],
        "نهم":   ["ریاضی", "علوم", "فارسی", "مطالعات", "پیام‌های آسمانی", "نگارش", "عربی", "انگلیسی"]
    },
    "دبیرستان": {
        "دهم": ["ریاضی", "فیزیک", "شیمی", "زیست", "عربی", "دینی", "فارسی", "نگارش", "هندسه", "آمار", "زبان", "زمین‌شناسی"],
        "یازدهم": ["ریاضی", "فیزیک", "شیمی", "زیست", "عربی", "دینی", "فارسی", "نگارش", "هندسه", "آمار", "زبان", "زمین‌شناسی"],
        "دوازدهم": ["ریاضی", "فیزیک", "شیمی", "زیست", "عربی", "دینی", "فارسی", "نگارش", "هندسه", "آمار", "زبان", "زمین‌شناسی"]
    },
    "پیام نور": {
        "عمومی": ["ریاضی", "آمار", "زبان", "معارف", "ادبیات"],
        "تخصصی": ["رشته‌های مختلف"]
    },
    "فنی و حرفه‌ای": {
        "دروس تخصصی": ["نمونه سوالات", "جزوات"]
    },
    "استخدامی": {
        "عمومی": ["هوش", "ادبیات", "معارف", "ریاضی", "کامپیوتر"],
        "تخصصی": ["رشته‌های مختلف"]
    }
}

# ------------------ قیمت خدمات ------------------
prices = {
    # خودرو
    "car_irankhodro": 150000,
    "car_saipa": 150000,
    "car_bahman": 150000,
    "car_taviz": 250000,

    # مسکن
    "house_amlak": 100000,
    "house_maskan": 50000,      # هر نفر
    "house_vadie": 700000,      # بسته وام ودیعه + خودنویس + شاهد

    # یارانه و کالابرگ
    "yarane_all": 60000,
    "kalabarg_all": 60000,

    # قضایی
    "ghazai_all": 35000,

    # دانشجویی
    "stu_entekhab": 100000,
    "stu_shahrieh": 35000,
    "stu_register": 300000,
    "stu_other": 50000,

    # عمومی
    "pub_sopishine": 80000,
    "pub_bime": 180000,
    "pub_darajeh": 200000,
    "pub_afsari": 200000,
    "pub_sakha": 100000,

    # بانکی
    "bank_iranzamin": 100000,
    "bank_mehr": 150000,
    "bank_blu": 0,
    "bank_other": 150000,
}

service_titles = {
    "car_irankhodro": "ثبت‌نام ایران‌خودرو",
    "car_saipa": "ثبت‌نام سایپا",
    "car_bahman": "ثبت‌نام بهمن خودرو",
    "car_taviz": "تعویض پلاک + خلافی + مالیات",

    "house_amlak": "املاک و اسکان",
    "house_maskan": "مسکن ملی (هر نفر)",
    "house_vadie": "بسته وام ودیعه + خودنویس + شاهد",

    "yarane_all": "تمام خدمات یارانه",
    "kalabarg_all": "تمام خدمات کالابرگ",

    "ghazai_all": "تمام خدمات قضایی",

    "stu_entekhab": "انتخاب واحد",
    "stu_shahrieh": "پرداخت شهریه",
    "stu_register": "ثبت‌نام دانشجویی",
    "stu_other": "سایر خدمات دانشجویی",

    "pub_sopishine": "سوءپیشینه",
    "pub_bime": "بیمه ورزشی",
    "pub_darajeh": "درجه‌داری",
    "pub_afsari": "افسری",
    "pub_sakha": "سخا",

    "bank_iranzamin": "افتتاح حساب ایران‌زمین",
    "bank_mehr": "افتتاح حساب مهر ایران",
    "bank_blu": "افتتاح حساب بلو بانک",
    "bank_other": "افتتاح حساب کشاورزی/صادرات/رفاه",
}

# ------------------ منوی اصلی ------------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📚 فروش فایل", callback_data="menu_files"),
        types.InlineKeyboardButton("🛠 خدمات", callback_data="menu_services")
    )
    bot.send_message(
        message.chat.id,
        "سلام 🌟\nبه سامانه جامع خدمات و فروش فایل خوش آمدید.\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data == "start_back")
def start_back(call):
    start(call.message)

# ------------------ منوی فروش فایل ------------------
@bot.callback_query_handler(func=lambda c: c.data == "menu_files")
def menu_files(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for level in subjects.keys():
        markup.add(types.InlineKeyboardButton(level, callback_data=f"level_{level}"))
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="start_back"))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📚 *انتخاب مقطع تحصیلی*\nیکی از مقاطع زیر را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("level_"))
def menu_grades(call):
    level = call.data.replace("level_", "")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for grade in subjects[level].keys():
        markup.add(types.InlineKeyboardButton(grade, callback_data=f"grade_{level}_{grade}"))
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_files"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        f"📘 *{level}*\nپایه مورد نظر را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("grade_"))
def menu_subjects(call):
    _, level, grade = call.data.split("_")
    markup = types.InlineKeyboardMarkup(row_width=1)
    for subject in subjects[level][grade]:
        markup.add(types.InlineKeyboardButton(subject, callback_data=f"subject_{level}_{grade}_{subject}"))
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data=f"level_{level}"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        f"📗 *{grade} — {level}*\nدرس مورد نظر را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("subject_"))
def menu_files_term(call):
    _, level, grade, subject = call.data.split("_")
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📄 نمونه سؤال ترم اول — 40,000 تومان",
                                   callback_data=f"file_{level}_{grade}_{subject}_term1"),
        types.InlineKeyboardButton("📄 نمونه سؤال ترم دوم — 40,000 تومان",
                                   callback_data=f"file_{level}_{grade}_{subject}_term2")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data=f"grade_{level}_{grade}"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        f"📄 *{subject} — {grade} — {level}*\nفایل مورد نظر را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ------------------ خرید فایل ------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith("file_"))
def file_selected(call):
    _, level, grade, subject, term = call.data.split("_")
    bot.send_message(
        call.message.chat.id,
        "برای ثبت سفارش، شماره موبایل خود را ارسال کنید.\n"
        "اگر مددجوی کمیته امداد یا بهزیستی هستید، بعد از شماره بنویسید: مددجو"
    )
    user_order_step[call.message.chat.id] = f"orderfile_{level}_{grade}_{subject}_{term}"

@bot.message_handler(func=lambda m: m.chat.id in user_order_step and user_order_step[m.chat.id].startswith("orderfile_"))
def process_file_order(message):
    step = user_order_step[message.chat.id]
    _, level, grade, subject, term = step.split("_")
    text = message.text.strip()

    is_madadjo = False
    if "مددجو" in text:
        is_madadjo = True
        phone = text.replace("مددجو", "").strip()
    else:
        phone = text

    base_price = 40000
    final_price, discount_text = get_final_price(base_price, is_madadjo, phone)

    file_customers[phone] = file_customers.get(phone, 0) + 1

    bot.send_message(
        ADMIN_ID,
        f"📥 *سفارش فایل جدید*\n\n"
        f"📘 مقطع: {level}\n"
        f"📗 پایه: {grade}\n"
        f"📙 درس: {subject}\n"
        f"📄 فایل: {'ترم اول' if term=='term1' else 'ترم دوم'}\n"
        f"💰 مبلغ قابل پرداخت: {final_price:,} تومان\n"
        f"📱 شماره مشتری: {phone}",
        parse_mode="Markdown"
    )

    bot.send_message(
        message.chat.id,
        f"{discount_text}"
        f"📄 سفارش شما ثبت شد.\n"
        f"💰 مبلغ قابل پرداخت: {final_price:,} تومان\n"
        "پس از پرداخت، فایل برای شما ارسال می‌شود.",
        parse_mode="Markdown"
    )

    user_order_step.pop(message.chat.id)

# ------------------ منوی خدمات ------------------
@bot.callback_query_handler(func=lambda c: c.data == "menu_services")
def menu_services(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🚗 خدمات خودرو", callback_data="service_car"),
        types.InlineKeyboardButton("🏠 خدمات مسکن", callback_data="service_house"),
        types.InlineKeyboardButton("🧾 یارانه و کالابرگ", callback_data="service_yarane"),
        types.InlineKeyboardButton("⚖️ خدمات قضایی", callback_data="service_ghazai"),
        types.InlineKeyboardButton("🎓 خدمات دانشجویی", callback_data="service_student"),
        types.InlineKeyboardButton("🧍 خدمات عمومی", callback_data="service_public"),
        types.InlineKeyboardButton("🏦 خدمات بانکی", callback_data="service_bank"),
        types.InlineKeyboardButton("🔙 بازگشت", callback_data="start_back")
    )
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🛠 *انتخاب دسته خدمات*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- خودرو
@bot.callback_query_handler(func=lambda c: c.data == "service_car")
def service_car(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("ایران‌خودرو — 150,000 تومان", callback_data="car_irankhodro"),
        types.InlineKeyboardButton("سایپا — 150,000 تومان", callback_data="car_saipa"),
        types.InlineKeyboardButton("بهمن خودرو — 150,000 تومان", callback_data="car_bahman"),
        types.InlineKeyboardButton("تعویض پلاک + خلافی + مالیات — 250,000 تومان", callback_data="car_taviz")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🚗 *خدمات خودرو*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- مسکن
@bot.callback_query_handler(func=lambda c: c.data == "service_house")
def service_house(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("املاک و اسکان — 100,000 تومان", callback_data="house_amlak"),
        types.InlineKeyboardButton("مسکن ملی (هر نفر 50,000 تومان)", callback_data="house_maskan"),
        types.InlineKeyboardButton("بسته وام ودیعه + خودنویس + شاهد — 700,000 تومان", callback_data="house_vadie")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🏠 *خدمات مسکن*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- یارانه
@bot.callback_query_handler(func=lambda c: c.data == "service_yarane")
def service_yarane(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("تمام خدمات یارانه — 60,000 تومان", callback_data="yarane_all"),
        types.InlineKeyboardButton("تمام خدمات کالابرگ — 60,000 تومان", callback_data="kalabarg_all")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🧾 *یارانه و کالابرگ*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- قضایی
@bot.callback_query_handler(func=lambda c: c.data == "service_ghazai")
def service_ghazai(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("تمام خدمات قضایی — 35,000 تومان", callback_data="ghazai_all")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "⚖️ *خدمات قضایی*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- دانشجویی
@bot.callback_query_handler(func=lambda c: c.data == "service_student")
def service_student(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("انتخاب واحد — 100,000 تومان", callback_data="stu_entekhab"),
        types.InlineKeyboardButton("پرداخت شهریه — 35,000 تومان", callback_data="stu_shahrieh"),
        types.InlineKeyboardButton("ثبت‌نام دانشجویی — 300,000 تومان", callback_data="stu_register"),
        types.InlineKeyboardButton("سایر خدمات دانشجویی — 50,000 تومان", callback_data="stu_other")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🎓 *خدمات دانشجویی*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- عمومی
@bot.callback_query_handler(func=lambda c: c.data == "service_public")
def service_public(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("سوءپیشینه — 80,000 تومان", callback_data="pub_sopishine"),
        types.InlineKeyboardButton("بیمه ورزشی — 180,000 تومان", callback_data="pub_bime"),
        types.InlineKeyboardButton("درجه‌داری — 200,000 تومان", callback_data="pub_darajeh"),
        types.InlineKeyboardButton("افسری — 200,000 تومان", callback_data="pub_afsari"),
        types.InlineKeyboardButton("سخا — 100,000 تومان", callback_data="pub_sakha")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🧍 *خدمات عمومی*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ---- بانکی
@bot.callback_query_handler(func=lambda c: c.data == "service_bank")
def service_bank(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("ایران‌زمین — 100,000 تومان", callback_data="bank_iranzamin"),
        types.InlineKeyboardButton("مهر ایران — 150,000 تومان", callback_data="bank_mehr"),
        types.InlineKeyboardButton("بلو بانک — رایگان", callback_data="bank_blu"),
        types.InlineKeyboardButton("کشاورزی/صادرات/رفاه — 150,000 تومان", callback_data="bank_other")
    )
    markup.add(types.InlineKeyboardButton("🔙 بازگشت", callback_data="menu_services"))
    bot.edit_message_text(
        call.message.chat.id,
        call.message.message_id,
        "🏦 *خدمات بانکی*\nیکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ------------------ انتخاب خدمت ------------------
@bot.callback_query_handler(func=lambda c: c.data.startswith(("car_", "house_", "yarane_", "kalabarg_", "ghazai_", "stu_", "pub_", "bank_")))
def service_selected(call):
    service_code = call.data
    chat_id = call.message.chat.id

    # مسکن ملی: نیاز به تعداد نفرات
    if service_code == "house_maskan":
        bot.send_message(
            chat_id,
            "مسکن ملی (هر نفر 50,000 تومان)\n"
            "لطفاً این‌طور ارسال کنید:\n"
            "تعداد نفرات - شماره موبایل\n"
            "مثال: 3 - 0912xxxxxxx\n"
            "اگر مددجو هستید، بعد از متن بنویسید: مددجو"
        )
    else:
        bot.send_message(
            chat_id,
            "برای ثبت سفارش، شماره موبایل خود را ارسال کنید.\n"
            "اگر مددجو هستید، بعد از شماره بنویسید: مددجو"
        )

    user_order_step[chat_id] = f"orderservice_{service_code}"

# ------------------ پردازش سفارش خدمات ------------------
@bot.message_handler(func=lambda m: m.chat.id in user_order_step and user_order_step[m.chat.id].startswith("orderservice_"))
def process_service_order(message):
    step = user_order_step[message.chat.id]
    _, service_code = step.split("_")
    text = message.text.strip()

    is_madadjo = False
    if "مددجو" in text:
        is_madadjo = True
        text = text.replace("مددجو", "").strip()

    # مسکن ملی (هر نفر)
    if service_code == "house_maskan":
        # فرمت: تعداد - شماره
        try:
            parts = [p.strip() for p in text.split("-")]
            count = int(parts[0])
            phone = parts[1]
        except Exception:
            bot.send_message(message.chat.id, "فرمت ورودی نادرست است. مثال: 3 - 0912xxxxxxx")
            return
        base_price = prices[service_code] * count
    else:
        phone = text
        base_price = prices.get(service_code, 0)

    final_price, discount_text = get_final_price(base_price, is_madadjo, phone)
    title = service_titles.get(service_code, service_code)

    bot.send_message(
        ADMIN_ID,
        f"🛠 *سفارش خدمت جدید*\n\n"
        f"🔧 خدمت: {title}\n"
        f"💰 مبلغ قابل پرداخت: {final_price:,} تومان\n"
        f"📱 شماره مشتری: {phone}",
        parse_mode="Markdown"
    )

    bot.send_message(
        message.chat.id,
        f"{discount_text}"
        f"🛠 سفارش شما ثبت شد.\n"
        f"💰 مبلغ قابل پرداخت: {final_price:,} تومان\n"
        "پس از پرداخت، خدمت انجام می‌شود.",
        parse_mode="Markdown"
    )

    user_order_step.pop(message.chat.id)

# ------------------ اجرای ربات ------------------
if __name__ == "__main__":
    bot.infinity_polling()