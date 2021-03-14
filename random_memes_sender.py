import logging

from dynaconf.utils.boxing import DynaBox
from telegram.ext import Updater, Dispatcher

from controllers import ChatController, InlineController
from config import settings
from models import init_database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def register_controllers(dispatcher: Dispatcher) -> None:
    ChatController(dispatcher=dispatcher, messages=settings.messages)
    InlineController(dispatcher=dispatcher, messages=settings.messages)


def main() -> None:
    init_database(settings.database.filename)
    updater = Updater(settings.bot.token)
    dispatcher = updater.dispatcher

    register_controllers(dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
