from typing import List

from gino.loader import ColumnLoader

from app.base.base_accessor import BaseAccessor
from app.game.models import Game, PlayerModel, GameModel, ListResponse, AnswersPlayersModel, Player, AnswersPlayers, \
    Winner
from app.store.database.gino import db


class GameAccessor(BaseAccessor):
    async def start_game(self, started_at: str) -> Game:
        raise NotImplementedError

    @staticmethod
    async def create_game(chat_id: int, started_at: str, duration: int) -> Game:
        obj = await GameModel.create(chat_id=chat_id, started_at=started_at, duration=duration)
        return obj.to_dc()

    @staticmethod
    async def create_players(players: List[Player]):
        await PlayerModel.insert().gino.all(
            [
                {
                    "vk_id": p.vk_id,
                    "first_name": p.first_name,
                    "last_name": p.last_name
                }
                for p in players
            ]
        )

    @staticmethod
    async def create_players_answers(ap: List[AnswersPlayers]):
        await AnswersPlayersModel.insert().gino.all(
            [
                {
                    "vk_id": a.vk_id,
                    "game_id": a.game_id
                }
                for a in ap
            ]
        )

    @staticmethod
    async def fetch_games() -> ListResponse:
        cnt = db.func.count(AnswersPlayersModel.id)
        obj = await GameModel.outerjoin(AnswersPlayersModel, GameModel.id == AnswersPlayersModel.game_id)\
            .select()\
            .group_by(GameModel.id, AnswersPlayersModel.vk_id)\
            .gino.load(GameModel.load(winner=Winner(vk_id=AnswersPlayersModel.vk_id, points=cnt))).all()
        return ListResponse(total=len(obj), games=[o.to_dc() for o in obj])

    async def fetch_game_stats(self):
        raise NotImplementedError
