from src.entity.score import Score
from src.entity.user import User
from src.entity.statistic import Statistic
from typing import List


class ScoreRepo:

    @staticmethod
    def scores_by_user(user: User) -> List[Score]:
        return list(Score.select().where(Score.user == user))

    @staticmethod
    def save(score: Score):
        score.save()

    @staticmethod
    def scores_to_scoreboard(scoreboard: Statistic) -> List[Score]:
        return list(Score.select().where(Score.board == scoreboard))
