from src.entity.score import Score
from src.entity.statistic import Statistic


class ScoreboardRepo:

    @staticmethod
    def get_scoreboard(time: int) -> Statistic:
        return Score.get_or_none(Statistic.time == time)

    @staticmethod
    def save(scoreboard: Statistic):
        scoreboard.save()
