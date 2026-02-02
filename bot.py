from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8564606214:AAEWnXWCLDjPhcPoZNAM91bPBUcz18L6-aE"
ADMIN_ID = 6047410515

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\nXabaringizni yozing, admin bilan bog'lanasiz.\n\n"
        "📎 Rasm, video, ovozli xabar, dokument ham yuborishingiz mumkin."
    )

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    user_info = (
        f"📩 Yangi xabar:\n"
        f"👤 Ism: {user.first_name or 'Noma\'lum'}\n"
    )
    
    if user.last_name:
        user_info += f"👤 Familiya: {user.last_name}\n"
    
    if user.username:
        user_info += f"🔗 Username: @{user.username}\n"
    
    user_info += f"🆔 ID: {user.id}\n\n"
    
    if update.message.text:
        user_info += f"📝 Xabar: {update.message.text}"
    elif update.message.photo:
        user_info += "🖼️ Rasm yuborildi"
        photo_file = await update.message.photo[-1].get_file()
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file.file_id,
            caption=user_info
        )
        return
    elif update.message.video:
        user_info += "🎬 Video yuborildi"
    elif update.message.voice:
        user_info += "🎤 Ovozli xabar yuborildi"
    elif update.message.document:
        user_info += f"📄 Dokument: {update.message.document.file_name}"
    else:
        user_info += "📎 Fayl yuborildi"
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    await update.message.reply_text("✅ Xabaringiz admin'ga yuborildi!")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Iltimos, foydalanuvchi xabariga reply qiling!")
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
                except (ValueError, IndexError):
                    await update.message.reply_text("❌ Foydalanuvchi ID'sini aniqlab bo'lmadi")
                    return
        
        if user_id:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"📨 Admin javobi:\n\n{update.message.text}"
                )
                await update.message.reply_text("✅ Javob foydalanuvchiga yuborildi!")
            except Exception as e:
                error_msg = str(e)
                if "Forbidden" in error_msg or "blocked" in error_msg.lower():
                    await update.message.reply_text("❌ Foydalanuvchi botni bloklagan yoki chat'ni yopgan")
                else:
                    await update.message.reply_text(f"❌ Xatolik: {error_msg}")
    else:
        await update.message.reply_text("❌ Bu xabarga javob berib bo'lmaydi")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    await update.message.reply_text(
        "👨‍💻 Admin paneliga xush kelibsiz!\n\n"
        "📝 Foydalanuvchi xabariga reply qilib javob bering!"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    await update.message.reply_text("📊 Statistikalar:\nHozircha statistikalar mavjud emas")


async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user.id == ADMIN_ID:
        return
    
    if update.message and update.message.text and not update.message.text.startswith('/'):
        await user_message(update, context)
    elif update.message:
        await user_message(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("stats", stats_command))
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.REPLY & filters.User(ADMIN_ID), 
        admin_reply
    ))
    
    app.add_handler(MessageHandler(
        filters.ALL & ~filters.COMMAND & ~filters.User(ADMIN_ID), 
        handle_all_messages
    ))
    
    print("✅ Bot ishga tushdi...")
    print(f"👑 Admin ID: {ADMIN_ID}")
    app.run_polling()

if name == "main":
    main()
