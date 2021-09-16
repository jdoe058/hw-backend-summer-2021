from app.game.models import WinnerInfo, Player
from app.store import Store
from tests.utils import ok_response, check_empty_table_exists


class TestPlayerStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "themes")

    async def test_create_theme(self, cli, store: Store):
        first_name = "John"
        last_name = "Doe"
        player = await store.games.add_player(first_name=first_name, last_name=last_name)
        assert type(player) is WinnerInfo
        assert player.last_name == last_name and player.first_name == first_name and player.vk_id == 1

        db = cli.app.database.db
        players = await Player.query.gino.all()
        assert len(players) == 1


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
