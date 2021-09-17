from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.game.schemes import ListResponseSchema, GameStatsSchema
from app.web.app import View
from aiohttp.web import HTTPForbidden, HTTPUnauthorized

from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        admin = await self.store.admins.get_by_email(email)
        if not admin or not admin.is_password_valid(password):
            raise HTTPForbidden
        admin_data = AdminSchema().dump(admin)
        response = json_response(data=admin_data)
        session = await new_session(request=self.request)
        session["admin"] = admin_data
        return response


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if self.request.admin:
            return json_response(data=AdminSchema().dump(self.request.admin))
        raise HTTPUnauthorized


class AdminFetchGamesView(AuthRequiredMixin, View):
    @response_schema(ListResponseSchema, 200)
    async def get(self):
        games = await self.store.games.fetch_games()
        return json_response(data=ListResponseSchema().dump(games))


class AdminFetchGameStatsView(AuthRequiredMixin, View):
    @response_schema(GameStatsSchema, 200)
    async def get(self):
        stats = {
            'games_average_per_day': 0,
            'winners_top': [],
            'duration_total': 0,
            'games_total': 0,
            'duration_average': 0

        }
        stat = await self.store.games.fetch_game_stats()
        return json_response(data=GameStatsSchema().dump(stats))
