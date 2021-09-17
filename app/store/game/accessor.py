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
        cnt_ = db.func.count(AnswersPlayersModel.id)
        query = db.select([
            GameModel, AnswersPlayersModel.vk_id, cnt_
        ]).select_from(
            GameModel.outerjoin(AnswersPlayersModel)
        ).group_by(
            GameModel.id, AnswersPlayersModel.vk_id
        )

        obj = await query.gino.load(
            GameModel.distinct(GameModel.id).load(winner=None)
        ).all()
        return ListResponse(total=len(obj), games=[o.to_dc() for o in obj])

    async def fetch_game_stats(self):
        sum_ = db.func.sum(GameModel.duration)
        avg_ = db.func.avg(GameModel.duration)
        cnt_ = db.func.count(GameModel.id)
        query = db.select([sum_, avg_, cnt_])
        obj = await query.gino.load(
            (ColumnLoader(sum_), ColumnLoader(avg_), ColumnLoader(cnt_))
        ).all()
        pass
