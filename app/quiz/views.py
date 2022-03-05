from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotFound
from aiohttp_apispec import response_schema, request_schema, querystring_schema

from app.quiz.schemes import (
    ThemeSchema, ThemeListSchema, QuestionSchema, ListQuestionSchema, ThemeIdSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data['title']
        for theme in await self.store.quizzes.list_themes():
            if title == theme.title:
                raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        raw_themes = {'themes': [ThemeSchema().dump(theme) for theme in themes]}
        return json_response(data=raw_themes)


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title, theme_id, answers = self.data['title'], self.data['theme_id'], self.data['answers']
        if self.store.quizzes.is_answers_valid(answers) is False:
            raise HTTPBadRequest
        if await self.store.quizzes.get_theme_by_id(theme_id) is None:
            raise HTTPNotFound
        if await self.store.quizzes.get_question_by_title(title) is not None:
            raise HTTPConflict
        question = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers= answers)
        raw_data = QuestionSchema().dump(question)
        return json_response(data=raw_data)


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = self.request.query.get('theme_id')
        try:
            if theme_id is not None:
                theme_id = int(theme_id)
        except ValueError:
            raise HTTPBadRequest
        questions = await self.store.quizzes.list_questions(theme_id)
        raw_data = {'questions': []}
        for question in questions:
            raw_data_question = QuestionSchema().dump(question)
            raw_data['questions'].append(raw_data_question)
        return json_response(data=raw_data)
