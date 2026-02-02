from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8564606214:AAEWnXWCLDjPhcPoZNAM91bPBUcz18L6-aE"
ADMIN_ID = 8564606214

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\nXabaringizni yozing,Muxitdinov bilan bog‘lanasiz."
    )

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    text = (
        f"📩 Yangi xabar:\n"
        f"👤 {user.first_name}\n"
        f"🔗 @{user.username}\n"
        f"🆔 {user.id}\n\n"
        f"{update.message.text}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        replied_text = update.message.reply_to_message.text.split("\n")

        for line in replied_text:
            if line.startswith("🆔"):
                user_id = int(line.replace("🆔", "").strip())
                await context.bot.send_message(
                    chat_id=user_id,
                    text="📨 Javob:\n" + update.message.text
                )
                break

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.User(ADMIN_ID), user_message))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))

print("✅ @iMukhitdinov_bot ishga tushdi...")
app.run_polling()
