from random import choice

from dynaconf.utils.boxing import DynaBox
from telegram import Update
from telegram.ext import Dispatcher, InlineQueryHandler, CallbackContext

from models.image_service import ImageService
from views import BotView


class InlineController:
    def __init__(self, dispatcher: Dispatcher, messages: DynaBox):
        self.dispatcher = dispatcher
        self.settings = messages
        self.view = BotView()
        self.service = ImageService()

        self.__process_handlers()

    def send_random_meme(self, update: Update, context: CallbackContext):
        images = self.service.read_all()
        meme_file_id = choice([image.file_id for image in images])

        self.view.send_inline_image(update, context, meme_file_id)

    def __process_handlers(self):
        main_handler = InlineQueryHandler(self.send_random_meme)
        self.dispatcher.add_handler(main_handler)
