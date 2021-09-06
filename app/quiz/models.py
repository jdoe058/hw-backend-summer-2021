from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy.orm import relationship

from app.store.database.gino import db


@dataclass
class Theme:
    id: Optional[int]
    title: str


class ThemeModel(db.Model):
    __tablename__ = "themes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)


# TODO
# Дописать все необходимые поля модели
class AnswerModel(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete="CASCADE"), nullable=False)


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list["Answer"]


# TODO
# Дописать все необходимые поля модели
class QuestionModel(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), nullable=False)

    answers = relationship('AnswerModel', cascade='all, delete')

    def __init__(self, **kw):
        super().__init__(**kw)

        self._answers: List[AnswerModel] = list()

    @property
    def answers(self) -> List[AnswerModel]:
        return self._answers

    @answers.setter
    def answers(self, val: Optional[AnswerModel]):
        if val is not None:
            self._answers.append(val)


@dataclass
class Answer:
    title: str
    is_correct: bool
