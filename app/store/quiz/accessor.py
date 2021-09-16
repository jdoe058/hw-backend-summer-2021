from typing import Optional, List
from sqlalchemy.sql.elements import or_

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Theme,
    Question,
    Answer,
    ThemeModel,
    QuestionModel,
    AnswerModel,
)


class QuizAccessor(BaseAccessor):
    @staticmethod
    async def create_theme(title: str) -> Theme:
        res = await ThemeModel.create(title=title)
        return res.to_dc()

    @staticmethod
    async def get_theme_by_title(title: str) -> Optional[Theme]:
        res = await ThemeModel.query.where(ThemeModel.title == title).gino.first()
        return None if res is None else res.to_dc()

    @staticmethod
    async def get_theme_by_id(id_: int) -> Optional[Theme]:
        res = await ThemeModel.get(id_)
        return None if res is None else res.to_dc()

    @staticmethod
    async def list_themes() -> List[Theme]:
        res = await ThemeModel.query.gino.all()
        return [r.to_dc() for r in res]

    @staticmethod
    async def create_answers(question_id, answers: List[Answer]):
        await AnswerModel.insert().gino.all(
            [
                {
                    "title": a.title,
                    "is_correct": a.is_correct,
                    "question_id": question_id
                }
                for a in answers
            ]
        )

    async def create_question(
        self, title: str, theme_id: int, answers: List[Answer]
    ) -> Question:
        obj = await QuestionModel.create(title=title, theme_id=theme_id)
        question = obj.to_dc()
        await self.create_answers(question.id, answers)
        question.answers = answers

        return question

    @staticmethod
    def _get_questions_join():
        return QuestionModel.outerjoin(AnswerModel, QuestionModel.id == AnswerModel.question_id).select()

    @staticmethod
    def _get_questions_load(query):
        return query.gino.load(QuestionModel.distinct(QuestionModel.id).load(answers=AnswerModel)).all()

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        query = self._get_questions_join().where(QuestionModel.title == title)
        questions = await self._get_questions_load(query)

        return None if not questions else questions[0].to_dc()

    async def list_questions(self, theme_id: Optional[int] = None) -> List[Question]:
        query = self._get_questions_join().where(or_(QuestionModel.theme_id == theme_id, theme_id is None))
        questions = await self._get_questions_load(query)

        return [q.to_dc() for q in questions]
