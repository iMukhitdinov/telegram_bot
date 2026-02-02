import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "8564606214:AAEWnXWCLDjPhcPoZNAM91bPBUcz18L6-aE"
SUPPORT_CHAT_ID = "-1005226559347"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Savolingizni yuboring, jamoa tez orada javob beradi.")

async def forward_to_staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    user_info = f"📩 Yangi xabar:\n👤 Foydalanuvchi: {user.first_name}\n🆔 ID: {user.id}\n💬 Xabar: {update.message.text}"
    
    if user.username:
        user_info = f"📩 Yangi xabar:\n👤 Foydalanuvchi: {user.first_name}\n🔗 Username: @{user.username}\n🆔 ID: {user.id}\n💬 Xabar: {update.message.text}"
    
    await context.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        text=user_info
    )

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != int(SUPPORT_CHAT_ID):
        return
    
    if update.message.reply_to_message:
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
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=f"📨 Support javobi:\n\n{update.message.text}"
                    )
                    await update.message.reply_text("✅ Javob yuborildi!")
                except:
                    await update.message.reply_text("❌ Foydalanuvchi botni bloklagan")

application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))

application.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND & ~filters.Chat(int(SUPPORT_CHAT_ID)),
    forward_to_staff
))

application.add_handler(MessageHandler(
    filters.TEXT & filters.Chat(int(SUPPORT_CHAT_ID)) & filters.REPLY,
    reply_to_user
))

print("🤖 Bot ishga tushdi...")
application.run_polling()
