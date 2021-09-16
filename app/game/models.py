from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Winner:
    vk_id: int
    points: int


@dataclass
class Game:
    id: str
    chat_id: int
    started_at: str
    duration: Optional[int]
    winner: Optional[Winner]
    finished_at: Optional[str]


@dataclass
class WinnerInfo:
    vk_id: int
    win_count: int
    first_name: str
    last_name: str


@dataclass
class GameStats:
    game_average_per_day: int
    winners_top: List[WinnerInfo]
    duration_total: int
    games_total: int
    duration_average: int
