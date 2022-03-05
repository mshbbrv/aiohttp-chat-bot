import typing
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


if typing.TYPE_CHECKING:
    from app.web.app import Application


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(
            id=self.app.database.next_theme_id,
            title=str(title)
        )
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if title.lower() == theme.title.lower():
                return theme
        return None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        for theme in self.app.database.themes:
            if id_ == theme.id:
                return theme
        return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        for question in self.app.database.questions:
            if title.lower() == question.title.lower():
                return question
        return None

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = Question(
            id=self.app.database.next_question_id,
            title=str(title),
            theme_id=int(theme_id),
            answers=answers
        )
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        list_questions = []
        if theme_id is not None:
            for question in self.app.database.questions:
                if question.theme_id == theme_id:
                    list_questions.append(question)
        else:
            list_questions = self.app.database.questions
        return list_questions

    @staticmethod
    def is_answers_valid(answers):
        count = 0
        for answer in answers:
            if answer['is_correct'] is True:
                count += 1
        if count != 1 or len(answers) <= 1:
            return False
        return True

    async def disconnect(self, app: "Application"):
        self.app.database.clear()

