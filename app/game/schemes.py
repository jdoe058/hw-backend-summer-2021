from marshmallow import Schema, fields


class WinnerScheme(Schema):
    vk_id = fields.Int(required=True)
    points = fields.Int(required=True)


class GameSchema(Schema):
    id = fields.Str(required=True)
    chat_id = fields.Int(required=True)
    started_at = fields.DateTime()
    duration = fields.Number()
    winner = fields.Nested(WinnerScheme)
    finished_at = fields.DateTime()


class ListResponseSchema(Schema):
    total = fields.Int(required=True)
    games = fields.Nested(GameSchema, many=True)


class WinnerInfoSchema(Schema):
    vk_id = fields.Int(required=True)
    win_count = fields.Int(required=True)
    first_name = fields.Str()
    last_name = fields.Str()


class GameStatsSchema(Schema):
    games_average_per_day = fields.Number()
    winners_top = fields.Nested(WinnerInfoSchema, many=True)
    duration_total = fields.Number()
    games_total = fields.Int()
    duration_average = fields.Number()
