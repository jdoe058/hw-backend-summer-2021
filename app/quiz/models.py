from dataclasses import dataclass
from typing import Optional

from app.store.database.gino import db


@dataclass
class Theme:
    id: Optional[int]
    title: str

# TODO
# Дописать все необходимые поля модели
class ThemeModel(db.Model):
    __tablename__ = "themes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)


# TODO
# Дописать все необходимые поля модели
class AnswerModel(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)


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
    title = db.Column(db.String)


@dataclass
class Answer:
    title: str
    is_correct: bool
