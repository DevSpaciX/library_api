import telegram

from library_core import settings


async def send_message_to_channel(
        bot_token=settings.TELEGRAM_BOT_TOKEN, chat_id=settings.TELEGRAM_CHAT_ID, text=None
):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=text)
