from app.base.base_accessor import BaseAccessor
from app.game.models import WinnerInfo, Game


class GameAccessor(BaseAccessor):
    async def start_game(self, started_at: str) -> Game:
        raise NotImplementedError

    async def add_player(self, first_name: str, last_name: str) -> WinnerInfo:
        raise NotImplementedError

    async def add_players_answers(self, vk_id: int):
        raise NotImplementedError
