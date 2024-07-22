from hmac import new
from typing import Final
from urllib import response
from telegram import Update
from telegram.ext import Application, CommandHandler, filters, ContextTypes, MessageHandler

with open('token.csv', "r") as token_file:
    token = token_file.readline()

TOKEN: Final = token
BOT_USERNAME: Final = '@word_gubot'



# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, here you can play Word Guess with one of your friends ...")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, here you can play Word Guess with one of your friends ... . (all the help message was this!)")

    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom command called!")


# Resposes

def handle_response(text: str) -> str:
    
    # processed: str = text.lower()

    if 'hello' in text.casefold():
        return 'Hey!'
    elif 'play' in text.casefold():
        return 'Game\'s unavailable for now, SORRY'
    else:
        return 'unknown text'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)



async def error(update: Update, context: ContextTypes):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':

    print('Starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling ...')
    app.run_polling(poll_interval=3)








