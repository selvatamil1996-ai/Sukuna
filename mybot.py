from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os

TOKEN = os.getenv("TOKEN")

# Welcome
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(
            f"🔥 Welcome {user.first_name} to Kasukabe Tamil Chat!"
        )

# ID
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 {update.effective_user.id}")

# Ban
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)

# Mute
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(update.effective_chat.id, user.id, permissions)

# Anti-link
async def filter_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "http" in update.message.text or "t.me" in update.message.text:
        await update.message.delete()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(CommandHandler("id", get_id))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_links))

app.run_polling()