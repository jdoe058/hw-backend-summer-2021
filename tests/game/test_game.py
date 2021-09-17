from datetime import datetime

import pytest
from app.game.models import WinnerInfo, Player, Game, GameModel
from app.store import Store
from tests.game import game2dict
from tests.utils import ok_response, check_empty_table_exists


class TestPlayerStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "players")

    # TO-DO понять почему id != 1!
    async def test_add_player(self, cli, store: Store):
        first_name = "John"
        last_name = "Doe"
        player = await store.games.create_player(first_name, last_name)
        assert type(player) is WinnerInfo
        assert player.last_name == last_name and player.first_name == first_name  # and player.vk_id == 1

        # db = cli.app.database.db
        players = await Player.query.gino.all()
        assert len(players) == 1


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
        assert data == ok_response(data={"total": 2, "games": [game2dict(game_2), game2dict(game_1)]})


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
