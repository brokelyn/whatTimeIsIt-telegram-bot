from src.entity.event import Event
from src.entity.score import Score
from src.entity.user import User


class ScoreRepo:

    @staticmethod
    def get_score(event: Event, user: User) -> Score:
        return Score.get_or_none(Score.event == event and Score.user == user)

    @staticmethod
    def save(score: Score):
        score.save()
