from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8564606214:AAEWnXWCLDjPhcPoZNAM91bPBUcz18L6-aE"
ADMIN_ID = 6047410515

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom!\nXabaringizni yozing, men bilan bog‘lanasiz.")

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "No Username"
    text = (
        f"📩 Yangi xabar:\n"
        f"👤 {user.first_name}\n"
        f"🔗 {username}\n"
        f"🆔 {user.id}\n\n"
        f"📝 Xabar:\n{update.message.text}"
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    except Exception:
        pass

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        replied_text = update.message.reply_to_message.text
        try:
            lines = replied_text.split("\n")
            user_id = None
            for line in lines:
                if "🆔" in line:
                    user_id = int(line.replace("🆔", "").strip())
                    break
            if user_id:
                await context.bot.send_message(chat_id=user_id, text=f"📨 :\n{update.message.text}")
                await update.message.reply_text("✅")
        except Exception:
            pass

if name == "main":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.User(ADMIN_ID), user_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID), admin_reply))
    app.run_polling()
