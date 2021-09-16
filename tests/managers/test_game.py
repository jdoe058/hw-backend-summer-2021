from tests.utils import ok_response


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
