from datetime import datetime
from typing import List

import pytest
from app.game.models import WinnerInfo, PlayerModel, Game, GameModel, Player, AnswersPlayersModel
from app.store import Store
from tests.fixtures import answers_players_games
from tests.game import game2dict
from tests.utils import ok_response, check_empty_table_exists


class TestPlayerStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "players")

    async def test_add_players(self, cli, store: Store, players: List[Player]):
        await store.games.create_players(players)

        obj = await PlayerModel.query.gino.all()
        assert [o.to_dc() for o in obj] == players


class TestGameStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "games")

    async def test_create_game(self, cli, store: Store):
        chat_id = 1
        started_at = datetime.strptime("21/09/06 16:30", "%d/%m/%y %H:%M")
        duration = 600
        game = await store.games.create_game(chat_id, started_at, duration)
        assert type(game) is Game
        assert game.chat_id == chat_id and game.duration == duration
        assert game.started_at == started_at

        games = await GameModel.query.gino.all()
        assert len(games) == 1

    async def test_create_players_answers(self, store: Store, answers_players_create):
        obj = await AnswersPlayersModel.query.gino.all()
        assert [o.to_dc() for o in obj] == answers_players_create


class TestAdminFetchGamesView:
    async def test_unauthorized(self, cli):
        resp = await cli.get("/admin.fetch_games")
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_different_method(self, authed_cli):
        resp = await authed_cli.post("/admin.fetch_games")
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"

    async def test_empty(self, authed_cli):
        resp = await authed_cli.get("/admin.fetch_games")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"total": 0, "games": []})

    async def test_one_game_without_players(self, authed_cli, game_1):
        resp = await authed_cli.get("/admin.fetch_games")
        assert resp.status == 200
        data = await resp.json()
        print(data)
        assert data == ok_response(data={"total": 1, "games": [game2dict(game_1)]})

    async def test_several_game_without_players(self, authed_cli, game_1, game_2):
        resp = await authed_cli.get("/admin.fetch_games")
        assert resp.status == 200
        data = await resp.json()
        print(data)
        assert data == ok_response(data={"total": 2, "games": [game2dict(game_1), game2dict(game_2)]})

    async def test_success1(self, authed_cli, answers_players_games):
        resp = await authed_cli.get("/admin.fetch_games")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"total": 3, "games": answers_players_games })


class TestAdminFetchGameStatsView:
    async def test_unauthorized(self, cli):
        resp = await cli.get("/admin.fetch_game_stats")
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_different_method(self, authed_cli):
        resp = await authed_cli.post("/admin.fetch_game_stats")
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"

    async def test_empty(self, authed_cli):
        resp = await authed_cli.get("/admin.fetch_game_stats")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data=
            {
                "games_average_per_day": 0,
                "winners_top": [],
                "games_total": 0,
                "duration_total": 0,
                "duration_average": 0,
            }
        )

    async def test_success2(self, authed_cli, answers_players_create):
        resp = await authed_cli.get("/admin.fetch_game_stats")
        assert resp.status == 200
        data = await resp.json()
