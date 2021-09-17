from dataclasses import dataclass
from typing import Optional, List

from app.store.database.gino import db


@dataclass
class Winner:
    vk_id: int
    points: int


@dataclass
class Game:
    id: int
    chat_id: int
    started_at: str
    duration: int
    # winner: Optional[Winner]
    finished_at: Optional[str]


@dataclass
class ListResponse:
    total: int
    games: List[Game]


class GameModel(db.Model):
    __tablename__ = "games"

    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    finished_at = db.Column(db.DateTime)

    def to_dc(self) -> Game:
        return Game(**self.to_dict())


@dataclass
class Player:
    vk_id: int
    first_name: str
    last_name: str


@dataclass
class WinnerInfo(Player):
    win_count: int


class PlayerModel(db.Model):
    __tablename__ = "players"

    vk_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def to_dc(self) -> Player:
        return Player(**self.to_dict())

    @property
    def count_win(self) -> int:
        return 0

    @property
    def points(self) -> int:
        return 0


@dataclass
class AnswersPlayers:
    vk_id: int
    game_id: int


class AnswersPlayersModel(db.Model):
    __tablename__ = "answers_players"

    id = db.Column(db.BigInteger, primary_key=True)
    vk_id = db.Column(db.ForeignKey("players.vk_id"), nullable=False)
    game_id = db.Column(db.ForeignKey("games.id"), nullable=False)
    # answer_id = db.Column(db.ForeignKey("answers.id"), nullable=False)

    def to_dc(self) -> AnswersPlayers:
        return AnswersPlayers(vk_id=self.vk_id, game_id=self.game_id)


@dataclass
class GameStats:
    game_average_per_day: int
    winners_top: List[WinnerInfo]
    duration_total: int
    games_total: int
    duration_average: int
