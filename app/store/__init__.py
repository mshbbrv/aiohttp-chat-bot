import typing

from app.store.bot.manager import BotManager
from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app

        from app.store.quiz.accessor import QuizAccessor
        from app.store.admin.accessor import AdminAccessor
        from app.store.telegram_api.accessor import TelegramBotApiAccessor

        self.quizzes = QuizAccessor(app)
        self.admins = AdminAccessor(app)
        self.bots_manager = BotManager(app)
        self.tg_bot_api = TelegramBotApiAccessor(app)


def setup_store(app: "Application"):
    app.database = Database()
    app.store = Store(app)
