from app.base.base_accessor import BaseAccessor
from app.game.models import WinnerInfo, Game, Player, GameModel, ListResponse, AnswersPlayers


class GameAccessor(BaseAccessor):
    async def start_game(self, started_at: str) -> Game:
        raise NotImplementedError

    @staticmethod
    async def create_game(chat_id: int, started_at: str, duration: int) -> Game:
        obj = await GameModel.create(chat_id=chat_id, started_at=started_at, duration=duration)
        return obj.to_dc()

    @staticmethod
    async def create_player(first_name: str, last_name: str) -> WinnerInfo:
        obj = await Player.create(first_name=first_name, last_name=last_name)
        return obj.to_dc()

    async def add_players_answers(self, vk_id: int):
        raise NotImplementedError

    @staticmethod
    async def fetch_games() -> ListResponse:
        obj = await GameModel.outerjoin(AnswersPlayers).select().gino.load(GameModel).all()
        return ListResponse(total=len(obj), games=[o.to_dc() for o in obj])

    async def fetch_game_stats(self):
        raise NotImplementedError
