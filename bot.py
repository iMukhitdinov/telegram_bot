from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8564606214:AAEWnXWCLDjPhcPoZNAM91bPBUcz18L6-aE"
ADMIN_ID = 6047410515

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Xabaringizni yozing, admin javob beradi.")

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_info = f"📩 Yangi xabar:\n👤 Ism: {user.first_name}\n🆔 ID: {user.id}\n📝 Xabar: {update.message.text}"
    
    if user.username:
        user_info = f"📩 Yangi xabar:\n👤 Ism: {user.first_name}\n🔗 Username: @{user.username}\n🆔 ID: {user.id}\n📝 Xabar: {update.message.text}"
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    await update.message.reply_text("✅ Xabaringiz admin'ga yuborildi!")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    if not update.message.reply_to_message:
        return
    
    reply_text = update.message.reply_to_message.text
    
    if "🆔 ID:" in reply_text:
        lines = reply_text.split("\n")
        user_id = None
        
        for line in lines:
            if "🆔 ID:" in line:
                try:
                    id_part = line.split("🆔 ID:")[1].strip()
                    user_id = int(id_part)
                    break
                except:
                    return
        
        if user_id:
            try:
                await context.bot.send_message(chat_id=user_id, text=f"📨 Admin javobi:\n{update.message.text}")
                await update.message.reply_text("✅ Javob yuborildi!")
            except:
                await update.message.reply_text("❌ Foydalanuvchi botni bloklagan")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.User(ADMIN_ID), user_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY & filters.User(ADMIN_ID), admin_reply))
    
    print("✅ Bot ishga tushdi...")
    app.run_polling()

if name == "main":
    main()
