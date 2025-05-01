import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, MessageHandler, CommandHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# تنظیم لاگ‌ها
logging.basicConfig(level=logging.INFO)

# دیکشنری موقت برای ذخیره آدرس‌های در انتظار تأیید
pending_links = {}

# دستور شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "لینک خود را ارسال کنید تا کد QR آن ساخته شود 📷\n"
        "اگر آدرس را بدون http/https وارد کنید، من از شما می‌پرسم کدام باشد. 😊"
    )

# دریافت متن و بررسی آدرس
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id

    if text.startswith("http://") or text.startswith("https://"):
        qr_url = f"https://qr-code.ir/api/qr-code?d={text}"
        await update.message.reply_photo(qr_url, caption="✅ کد QR لینک شما:")
    else:
        # ذخیره لینک در انتظار برای این کاربر
        pending_links[user_id] = text

        keyboard = [
            [
                InlineKeyboardButton("🔒 https://", callback_data="https"),
                InlineKeyboardButton("🌐 http://", callback_data="http")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "❓ لینک شما بدون http/https ارسال شده است.\n"
            "لطفاً مشخص کنید لینک شما با کدام شروع می‌شود:",
            reply_markup=reply_markup
        )

# پاسخ به انتخاب نوع http/https
async def handle_protocol_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    protocol = query.data
    user_id = query.from_user.id

    if user_id not in pending_links:
        await query.edit_message_text("❌ لینک موقتی یافت نشد. لطفاً دوباره ارسال کنید.")
        return

    final_url = f"{protocol}://{pending_links.pop(user_id)}"
    qr_url = f"https://qr-code.ir/api/qr-code?d={final_url}"

    await query.edit_message_text(f"✅ لینک نهایی: {final_url}")
    await query.message.reply_photo(qr_url, caption="📷 کد QR لینک شما:")

# اجرای ربات

TOKEN = "7994165255:AAHPreh7RuCnfFm-zIqAsHiTe0u6-ZtG21M"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(handle_protocol_choice))

app.run_polling()
