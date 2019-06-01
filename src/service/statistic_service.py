from src.entity.score import Score
from src.entity.user import User
from src.entity.statistic import Statistic
from src.repo.score_repo import ScoreRepo

from typing import Dict


class StatisticService:

    @staticmethod
    def extract_scores(scoreboard: Statistic) -> Dict[str, str]:
        pass

    @staticmethod
    def html_presentation(board: Dict[str, str]) -> str:
        return "No Scores"
