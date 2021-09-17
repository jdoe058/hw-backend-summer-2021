from datetime import datetime

import pytest

from app.game.models import Game


@pytest.fixture
async def game_1(store) -> Game:
    game = await store.games.create_game(
        chat_id=1,
        started_at=datetime.strptime("21/09/06 16:30", "%d/%m/%y %H:%M"),
        duration=600
    )
    yield game


@pytest.fixture
async def game_2(store) -> Game:
    game = await store.games.create_game(
        chat_id=2,
        started_at=datetime.strptime("21/09/07 11:30", "%d/%m/%y %H:%M"),
        duration=900
    )
    yield game
