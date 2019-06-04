from entity.score import Score
from entity.user import User
from entity.statistic import Statistic
from typing import List


class ScoreRepo:

    @staticmethod
    def scores_by_user(user: User) -> List[Score]:
        return list(Score.select().where(Score.user == user))

    @staticmethod
    def save(score: Score):
        score.save()

    @staticmethod
    def create(score: Score):
        score.save(force_insert=True)

    @staticmethod
    def scores_to_stat(stat: Statistic) -> List[Score]:
        return list(Score.select().where(Score.stat == stat))

    @staticmethod
    def save_or_create(score: Score):
        score = Score.select().where(Score.id == score.id)
        if not score:
            ScoreRepo.create(score)
        else:
            ScoreRepo.save()
