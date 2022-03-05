from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Boolean(required=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int()


class QuestionSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema))


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema))


class ListQuestionSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema))
