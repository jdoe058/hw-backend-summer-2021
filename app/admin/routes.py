import typing

from app.admin.views import AdminCurrentView

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.admin.views import AdminLoginView, AdminFetchGamesView, AdminFetchGameStatsView

    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.current", AdminCurrentView)
    app.router.add_view("/admin.fetch_games", AdminFetchGamesView)
    app.router.add_view("/admin.fetch_game_stats", AdminFetchGameStatsView)
