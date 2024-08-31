import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from llm import llm_reply, personality_system_prompt
from check_payment import check_payment
from constants import TG_BOT_TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


CHAT_HISTORY = {}
USER_PAYMENTS = {}

PAYMENT = 0
PAYMENT_CHECK = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # intialize a user
    user = update.message.chat_id
    CHAT_HISTORY[user] = {"messages": []}
    USER_PAYMENTS[user] = False # user has not paid yet to use the bot

    reply_keyboard = [["Architects INTJ ❤️", "Logisticians ISTJ ❤️"]]

    await update.message.reply_text(
        "Hi :) I'm your personalized Girlfriend ☺️\nSelect the personality type you want to vibe with 🥰",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Pick my personality 👇"
        ),
    )

    return PAYMENT



async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.chat_id
    personality_type_text = update.message.text # personalty type given by the user
    
    if len(CHAT_HISTORY[user]["messages"]) == 0:
        CHAT_HISTORY[user]["messages"].append(
            personality_system_prompt(personality_type_text)
        )

    await update.message.reply_text("If you want me so bad, you'll have to show it 😉\nGive me some BNB to talk to me 😛\n\n0xfba9a270Ac51bAEf134fE4F9D2DbDd539B9fd261")
    await update.message.reply_text("When you finish don't forget about me and text me back with the transaction hash ;)")

    return PAYMENT_CHECK


async def payment_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.chat_id
    tx_hash = update.message.text # tx_hash given by the user
    paid = check_payment(tx_hash)
    
    if paid:
        USER_PAYMENTS[user] = paid # user has paid
        await update.message.reply_text("Tell me anything you want :)")
        return ConversationHandler.END
    
    await update.message.reply_text("YOU DON'T LOVE ME?? PAY OR GO AWAY 😡\nI guess I'll talk to someone who actually loves me 🙄")
    return PAYMENT
    


async def discuss(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.chat_id

    user_message = update.message.text
    CHAT_HISTORY[user]["messages"].append(
        {
            'role': 'user',
            'content': user_message,
        }
    )


    ai_gf_reply = llm_reply(CHAT_HISTORY[user]["messages"])
    CHAT_HISTORY[user]["messages"].append(
        {
            'role': 'assistant',
            'content': ai_gf_reply,
        }
    )

    await update.message.reply_text(ai_gf_reply)





async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TG_BOT_TOKEN).build()

    # Initial conversation handler flow for choosing personality types + accepting payment
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PAYMENT: [MessageHandler(filters.TEXT, payment)],
            PAYMENT_CHECK: [MessageHandler(filters.TEXT, payment_check)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # on non command i.e message - dialogue with GF
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, discuss))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()