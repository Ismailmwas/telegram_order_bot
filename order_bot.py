from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your bot token and your Telegram ID
TOKEN = "8465537862:AAFo_6SXfMy5fcVEWOIZm96_XFF6yDZGDI4"
ADMIN_ID = 1803902612

# Shop items
ITEMS = {
    "001": {"name": "T-shirt", "price": 500},
    "002": {"name": "Shoes", "price": 1200},
    "003": {"name": "Cap", "price": 300},
    "004": {"name": "panty", "price": 30},
}

# Start command - show product list
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{item['name']} - Ksh {item['price']}", callback_data=item_id)]
        for item_id, item in ITEMS.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select the item you want to order:", reply_markup=reply_markup)

# When user selects an item
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    item_id = query.data
    item = ITEMS[item_id]

    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm Order", callback_data=f"confirm_{item_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"You selected *{item['name']}* for *Ksh {item['price']}*.\nDo you want to confirm?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# When user confirms or cancels
async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    username = user.username or user.first_name

    if query.data.startswith("confirm_"):
        item_id = query.data.split("_")[1]
        item = ITEMS[item_id]
        await query.edit_message_text(f"✅ Order confirmed: {item['name']} for Ksh {item['price']}.")
        
        # Notify admin (you)
        message = (
            f"🛒 New Order!\n"
            f"Customer: @{username}\n"
            f"Item: {item['name']}\n"
            f"Price: Ksh {item['price']}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=message)

    elif query.data == "cancel":
        await query.edit_message_text("❌ Order cancelled.")

# Build the bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(confirm_order, pattern="^(001|002|003)$"))
app.add_handler(CallbackQueryHandler(handle_action, pattern="^(confirm_|cancel)"))

print("Bot is running and will send you new orders...")
app.run_polling()
