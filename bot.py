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
