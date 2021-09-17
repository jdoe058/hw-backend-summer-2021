from typing import Optional

from app.game.models import Game, Winner, WinnerInfo


def game2dict(game: Game, winner: Optional[Winner] = None):
    return {
        "id": int(game.id),
        "chat_id": int(game.chat_id),
        "started_at": str(game.started_at),
        "duration": int(game.duration),
        "finished_at": game.finished_at,
        "winner": None if winner is None else winner2dict(winner)
    }


def winner2dict(win: Winner):
    return {
        "vk_id": int(win.vk_id),
        "points": int(win.points)
    }


def winfo2dict(info: WinnerInfo):
    return {
        "vk_id": int(info.vk_id),
        "win_count": int(info.win_count),
        "first_name": str(info.first_name),
        "last_name": str(info.last_name)
    }
