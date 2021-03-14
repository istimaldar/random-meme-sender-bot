from typing import List, Tuple, Any
from uuid import uuid4

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultCachedPhoto
from telegram.ext import CallbackContext

MenuItems = List[str]


class BotView:
    @staticmethod
    def send_message(update: Update, context: CallbackContext, text: str) -> None:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    @staticmethod
    def send_image(update: Update, context: CallbackContext, file_id: str, caption: str = None) -> None:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_id, caption=caption)

    @staticmethod
    def send_menu(update: Update, _: CallbackContext, message: str, id_: int, items: MenuItems) -> None:
        buttons = []
        for item in items:
            buttons.append(InlineKeyboardButton(text=item, callback_data=f'{id_}#{item}'))

        markup = InlineKeyboardMarkup([buttons])
        update.message.reply_text(message, reply_markup=markup)

    @staticmethod
    def send_inline_image(update: Update, _: CallbackContext, file_id: str):
        result = [InlineQueryResultCachedPhoto(id=str(uuid4()), photo_file_id=file_id)]
        update.inline_query.answer(result, cache_time=0)

