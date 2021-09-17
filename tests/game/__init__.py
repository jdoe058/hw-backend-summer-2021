from datetime import *
from app.game.models import Game


def game2dict(game: Game):
    return {
        "id": int(game.id),
        "chat_id": int(game.chat_id),
        "started_at": str(game.started_at),
        "duration": int(game.duration),
        "finished_at": game.finished_at
    }
