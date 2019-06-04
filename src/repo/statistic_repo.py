from src.entity.score import Score
from src.entity.statistic import Statistic
from typing import List


class StatisticRepo:

    @staticmethod
    def save(stat: Statistic):
        stat.save()

    @staticmethod
    def create(stat: Statistic):
        stat.save(force_insert=True)

    @staticmethod
    def get_or_none(time: int) -> Statistic:
        return Statistic.get_or_none(Statistic.time == time)

    @staticmethod
    def get_or_create(time: int):
        stat = StatisticRepo.get_or_none(time)
        if not stat:
            stat = Statistic(time=time)
            StatisticRepo.create(stat)
        return stat
