from app.base.base_accessor import BaseAccessor
from app.game.models import WinnerInfo, Game, Player


class GameAccessor(BaseAccessor):
    async def start_game(self, started_at: str) -> Game:
        raise NotImplementedError

    @staticmethod
    async def add_player(first_name: str, last_name: str) -> WinnerInfo:
        obj = await Player.create(first_name=first_name, last_name=last_name)
        return obj.to_dc()

    async def add_players_answers(self, vk_id: int):
        raise NotImplementedError
