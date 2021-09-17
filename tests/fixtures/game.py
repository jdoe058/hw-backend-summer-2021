from datetime import datetime
from typing import List

import pytest

from app.game.models import Game, Player, AnswersPlayers


@pytest.fixture
def players(store) -> List[Player]:
    return [
        Player(vk_id=1, first_name="First", last_name="Player"),
        Player(vk_id=2, first_name="Second", last_name="Player"),
        Player(vk_id=3, first_name="Other", last_name="Player")
    ]


@pytest.fixture
async def answers_players(store, players, game_1, game_2) -> List[AnswersPlayers]:
    ap = [
        AnswersPlayers(game_id=game_1.id, vk_id=players[0].vk_id),
        AnswersPlayers(game_id=game_1.id, vk_id=players[0].vk_id),
        AnswersPlayers(game_id=game_1.id, vk_id=players[1].vk_id),
        AnswersPlayers(game_id=game_2.id, vk_id=players[1].vk_id),
        AnswersPlayers(game_id=game_2.id, vk_id=players[1].vk_id),
        AnswersPlayers(game_id=game_2.id, vk_id=players[2].vk_id),
    ]
    await store.games.create_players(players)
    await store.games.create_players_answers(ap)

    yield ap


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
