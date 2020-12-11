from entity.statistic import Statistic


class StatisticRepo:

    @staticmethod
    def save(stat: Statistic):
        stat.save()

    @staticmethod
    def create(stat: Statistic):
        stat.save(force_insert=True)

    @staticmethod
    def get_or_none(group_id: int, time: int) -> Statistic:
        return Statistic.get_or_none(Statistic.time == time, Statistic.group == group_id)

    @staticmethod
    def get_or_create(group_id: int, time: int):
        stat = StatisticRepo.get_or_none(group_id, time)
        if not stat:
            stat = Statistic(time=time, group=group_id)
            StatisticRepo.create(stat)
        return stat
