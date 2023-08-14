from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


from decouple import Config, RepositoryEnv

from db import DATABASE
from get_image import IMAGE
from util import creative_sentences
from random import choices

config = Config(RepositoryEnv('.env'))

BOT_TOKEN = config('BOT_TOKEN')
channel_name = config('CHANNEL_NAME')
log_channel = config('LOG_CHANNEL')
db = DATABASE()
img = IMAGE()


def start(update, context):
    update.message.reply_text(
        "👋 Greetings! I'm here to assist you. To explore all the amazing things I can do, simply send /help. 🚀")


def help(update, context):

    update.message.reply_text('🤖 **Available Commands:**\n\n'
                              '🚀 /start  Start/Restart the bot\n'
                              '🖋️ /prompt  Send a prompt to generate an image\n'
                              '📜 /rules  Show the rules\n'
                              '❓ /help  Show this help message\n'
                              '⚙️ /settings  Account settings `under construction`\n'
                              '🔑 /register  Register to this service\n'
                              '💳 /payment  Payment information `under construction`\n'
                              '📞 /contactMe  \n'
                              '✉️ /feedback  \n', parse_mode='MarkdownV2')


def rules(update, context):
    update.message.reply_text(f"🌟 Welcome, {update.message.chat.username}!\n\n"
                              "✨ Here are the rules to create a safe and positive community within our bot:\n\n"
                              'Rule 1: \n'
                              'Rule 2: \n'
                              'Rule 3: \n'
                              'Rule 4: \n'
                              )


def recive_phone_number(update, context):
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        if not db.get_data({"username": update.message.chat.username}):
            db.add_data(
                {
                    "username": f"{update.message.chat.username}",
                    "phone_number": f"{phone_number}"
                }
            )
            update.message.reply_text(
                f"🎉 Bravo, {update.message.chat.username}!all set to unleash your creativity! 🎨\n\n"
                "📌 Use the mighty /prompt command to send your artistic prompt:\n"
                "`/prompt 'your prompt'`\n"
                "💡 Feel free to get creative!", reply_markup=ReplyKeyboardRemove())
            context.bot.send_message(
                log_channel, f'New User Registered, {update.message.chat.username}-{phone_number}')
        else:
            update.message.reply_text(
                f"🌟 Greetings, {update.message.username}! You're already a part of the creative journey! 🎨\n\n"
                "Feel free to send prompts using the /prompt command:\n"
                "🚀 Launch your imagination with the powerful /prompt command:\n"
                "✨ Let's get creative!", reply_markup=ReplyKeyboardRemove())

    else:
        update.message.reply_text(
            "Please use the provided keyboard to share your phone number 📱")


def register(update, context):
    keyboard = [
        [KeyboardButton(text="Share Phone Number", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        "Please use the provided keyboard to share your phone number 📱", reply_markup=reply_markup
    )


def prompt(update, context):
    prompt = update.message.text[len('/prompt '):]
    # prompt = "shot of vaporwave fashion dog in miami"
    image = img.get_image(prompt)

    like_button = InlineKeyboardButton(
        "👍 ", callback_data=f"like_{update.message.message_id}")
    dislike_button = InlineKeyboardButton(
        "👎 ", callback_data=f"dislike_{update.message.message_id}")
    keyboard = [[like_button, dislike_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if not db.get_data({"username": update.message.chat.username}):
        update.message.reply_text(
            f"⏲️ Your image will be uploaded to {channel_name} shortly! 🎉")
        message_sent = context.bot.send_photo(channel_name, image, caption=f"🎨 **Art Inspiration!**\n\n"
                                              f"📌 Prompt: {prompt}\n"
                                              f"👤 By: @{update.message.from_user.username}\n\n"
                                              f"🌟 {choices(creative_sentences)[0]} 🚀", reply_markup=reply_markup)
        # context.bot.send_message(
        #     channel_name, "in sort time", reply_markup=reply_markup)
        context.bot.send_message(
            log_channel, f'New Prompt from {update.message.chat.username}')
        message_sent.forward(log_channel)

    else:
        message_sent_private = context.bot.send_photo(update.message.chat.id, image,
                                                      caption=f"🎨 **Art Inspiration!**\n\n"
                                                      f"📌 Prompt: {prompt}\n"
                                                      f"👤 By: @{update.message.from_user.username}\n\n"
                                                      f"🌟 {choices(creative_sentences)[0]} 🚀")
        message_sent_private.forward(log_channel)
        # context.bot.send_message(
        #     update.message.chat.id, "in sort time here", reply_markup=reply_markup)


def button_click(update, context) -> None:
    query = update.callback_query
    button_data = query.data.split('_')

    # Extracting the action and message ID from button data
    action = button_data[0]
    message_id = int(button_data[1])

    # Handling different button actions
    if action == 'like':
        context.bot.answer_callback_query(query.id, text="You liked the post!")
    elif action == 'dislike':
        context.bot.answer_callback_query(
            query.id, text="You disliked the post!")


def feedback(update, context):
    feedback = update.message.text[len('/feedback '):]
    context.bot.send_message(
        log_channel, f'New Feedback from, {update.message.chat.username}-{feedback}')


app = "place holder"


def main() -> None:
    updater = Updater(BOT_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("prompt", prompt))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(MessageHandler(Filters.contact, recive_phone_number))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
