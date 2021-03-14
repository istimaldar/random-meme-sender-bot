from enum import Enum
from re import compile
from typing import Optional, List

from dynaconf.utils.boxing import DynaBox
from pony.orm import TransactionIntegrityError
from telegram import Update
from telegram.ext import Dispatcher, ConversationHandler, CallbackContext, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler, Handler

from models.database import Image
from models.image_service import ImageService
from views import BotView


class States(Enum):
    READY = 0
    WAITING = 1
    LISTED = 2
    SELECTED = 3


class ChatController:
    CAPTION_REGEX = compile('^[A-zА-яЁёІіЎў_. \'-]+$')
    NUMBER_REGEX = compile('^[0-9]+$')

    def __init__(self, dispatcher: Dispatcher, messages: DynaBox):
        self.dispatcher = dispatcher
        self.settings = messages
        self.view = BotView()
        self.service = ImageService()

        self.__process_handlers()

    def start(self, update: Update, context: CallbackContext) -> States:
        self.view.send_message(update, context, self.settings.start)
        return States.READY

    def help(self, update: Update, context: CallbackContext) -> States:
        self.view.send_message(update, context, self.settings.help)
        return States.READY

    def privacy(self, update: Update, context: CallbackContext) -> States:
        self.view.send_message(update, context, self.settings.privacy)
        return States.READY

    def add_meme(self, update: Update, context: CallbackContext) -> States:
        self.view.send_message(update, context, self.settings.add_meme)
        return States.WAITING

    def upload(self, update: Update, context: CallbackContext) -> States:
        if self.__validate_upload_message(update, context):
            self.__save_image(update, context)

        return States.READY

    def list(self, update: Update, context: CallbackContext) -> States:
        photos_list = self.__get_memes_list_message()
        self.view.send_message(update, context, photos_list)

        return States.LISTED

    def button_handler(self, update: Update, context: CallbackContext) -> States:
        id_, action = update.callback_query.data.split('#')
        if action == self.settings.buttons.delete:
            self.service.delete(int(id_))
            self.view.send_message(update, context, self.settings.select.deleted)
        elif action == self.settings.buttons.cancel:
            self.view.send_message(update, context, self.settings.select.canceled)

        return States.READY

    def select(self, update: Update, context: CallbackContext) -> States:
        resulting_state = States.READY
        meme = self.__get_meme_by_query(update, context)
        if meme is None:
            self.view.send_message(update, context, self.settings.select.not_found)
        else:
            self.__print_image_menu(update, context, meme)
            resulting_state = States.SELECTED

        return resulting_state

    def __print_image_menu(self, update: Update, context: CallbackContext, image: Image) -> None:
        self.view.send_image(update, context, image.file_id, image.name)
        self.view.send_menu(update, context, self.settings.buttons.caption, image.id, [
            self.settings.buttons.delete,
            self.settings.buttons.cancel
        ])

    def __get_meme_by_query(self, update: Update, context: CallbackContext) -> Optional[Image]:
        result = None
        query = update.message.text
        if self.NUMBER_REGEX.match(query):
            result = self.service.read_by_id(int(query))
        elif self.CAPTION_REGEX.match(query):
            result = self.service.read_by_name(query)
        else:
            self.view.send_message(update, context, self.settings.select.invalid_format)

        return result

    def __get_memes_list_message(self) -> str:
        images = self.service.read_all()
        lines = [self.settings.list.image_select] + [f'{image.id}. {image.name}' for image in images]
        return '\n'.join(lines)

    def __validate_upload_message(self, update: Update, context: CallbackContext) -> bool:
        success = True

        if len(update.message.photo) == 0 and update.message.document is None:
            self.view.send_message(update, context, self.settings.upload.no_image)
            success = False

        if update.message.caption is None or update.message.caption == '':
            self.view.send_message(update, context, self.settings.upload.no_caption)
            success = False

        elif not self.CAPTION_REGEX.match(update.message.caption):
            self.view.send_message(update, context, self.settings.upload.invalid_caption)
            success = False

        return success

    def __save_image(self, update: Update, context: CallbackContext) -> None:
        photo = update.message.photo[-1] if len(update.message.photo) > 0 else update.message.document
        name = update.message.caption

        try:
            self.service.create(name, photo.file_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.settings.upload.success)
        except TransactionIntegrityError:
            context.bot.send_message(chat_id=update.effective_chat.id, text=self.settings.upload.duplicated_caption)

    def __process_handlers(self):
        ready_handlers = [
            CommandHandler('help', self.help),
            CommandHandler('privacy', self.privacy),
            CommandHandler('add_meme', self.add_meme),
            CommandHandler('memes', self.list),
        ]  # type: List[Handler[Update]]
        waiting_handlers = [
            MessageHandler(Filters.all, self.upload)
        ]  # type: List[Handler[Update]]
        listed_handlers = [
            MessageHandler(Filters.all, self.select)
        ]  # type: List[Handler[Update]]
        selected_handlers = [
            CallbackQueryHandler(self.button_handler)
        ]  # type: List[Handler[Update]]
        states = {
            States.READY: ready_handlers,
            States.WAITING: ready_handlers + waiting_handlers,
            States.LISTED: ready_handlers + listed_handlers,
            States.SELECTED: ready_handlers + selected_handlers
        }
        main_handler = ConversationHandler(entry_points=[CommandHandler('start', self.start)],
                                           states=states, fallbacks=[], allow_reentry=True)
        self.dispatcher.add_handler(main_handler)
