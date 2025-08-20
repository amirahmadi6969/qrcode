from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

TOKEN = '7994165255:AAHPreh7RuCnfFm-zIqAsHiTe0u6-ZtG21M'
# پاسخ به پیام متنی
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    # ارسال به API هوش مصنوعی (مثلاً HuggingFace یا DuckDuckGo)
    response = requests.get(f"https://api.duckduckgo.com/?q={question}&format=json").json()
    answer = response.get("AbstractText", "متأسفم، پاسخی پیدا نشد.")
    await update.message.reply_text(answer)

# پاسخ به تصویر
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_url = photo_file.file_path
    # ارسال تصویر به API تحلیل تصویر (مثلاً Imagga)
    response = requests.get(f"https://api.imagga.com/v2/tags?image_url={photo_url}",
                            headers={"Authorization": "Basic YOUR_API_KEY"}).json()
    tags = [tag['tag']['en'] for tag in response['result']['tags'][:3]]
    await update.message.reply_text(f"📷 تصویر شامل: {', '.join(tags)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.run_polling()


