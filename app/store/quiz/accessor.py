from typing import Optional

from aiohttp.web_exceptions import HTTPException

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Theme,
    Question,
    Answer,
    ThemeModel,
    QuestionModel,
    AnswerModel,
)
from typing import List


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        res = await ThemeModel.create(title=title)
        return Theme(**res.to_dict())


    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        res = await ThemeModel.query.where(ThemeModel.title == title).gino.first()
        return Theme(**res.to_dict()) if res else None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        res = await ThemeModel.query.where(ThemeModel.id == id_).gino.first()
        return Theme(**res.to_dict()) if res else None

    async def list_themes(self) -> List[Theme]:
        res = await ThemeModel.query.gino.all()
        return [Theme(**r.to_dict()) for r in res]

    async def create_answers(self, question_id, answers: List[Answer]):
        raise NotImplementedError

    async def create_question(
        self, title: str, theme_id: int, answers: List[Answer]
    ) -> Question:
        raise NotImplementedError

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        raise NotImplementedError

    async def list_questions(self, theme_id: Optional[int] = None) -> List[Question]:
        raise NotImplementedError
