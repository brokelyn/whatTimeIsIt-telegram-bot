import collections
from typing import Dict

from entity.score import Score
from entity.user import User
from entity.statistic import Statistic
from repo.score_repo import ScoreRepo
from repo.message_repo import MessageRepo
from repo.statistic_repo import StatisticRepo
from service.time_service import TimeService


class StatisticService:

    @staticmethod
    def extract_scores_from_statistic(stat: Statistic) -> Dict[User, Score]:
        scores = ScoreRepo.scores_to_stat(stat)

        user_score = dict()
        for score in scores:
            user_score[score.user] = score

        return user_score

    @staticmethod
    def sort_dict(stats: Dict[User, int]) -> Dict[User, int]:
        sorted_x = sorted(stats.items(), key=lambda kv: kv[1])
        sorted_x.reverse()
        return collections.OrderedDict(sorted_x)

    @staticmethod
    def calc_stats(stat: Statistic):
        pattern = str(stat.time)
        messages = MessageRepo.findByIdIsGreater(stat.last_msg_id)

        if len(messages) == 0:
            return

        user_score_dict = StatisticService.extract_scores_from_statistic(stat)

        last_user_list = []

        for msg in messages:
            time_tz = TimeService.datetime_correct_tz(msg.time)
            msg_date: int = int(time_tz.strftime('%Y%m%d'))
            msg_time: int = int(time_tz.strftime('%H%M'))
            if msg_time == stat.time:
                if pattern in msg.text:
                    if msg.user not in user_score_dict:
                        new_score = Score(user=msg.user, stat=stat)
                        user_score_dict[msg.user] = new_score
                    if msg_date > user_score_dict[msg.user].date:
                        user_score_dict[msg.user].points += 1
                        user_score_dict[msg.user].date = msg_date
                        if msg.user not in last_user_list:
                            last_msg = msg
                            last_user_list.append(last_msg.user)

        if len(last_user_list) > 1:
            user_score_dict[last_user_list[-1]].points += 1

        for score in user_score_dict.values():
            ScoreRepo.save(score)

        stat.last_msg_id = messages[-1].id
        StatisticRepo.save(stat)

    @staticmethod
    def get_statistic_rank(stats: Dict[User, Score], user_to_find: User) -> int:
        index = 0
        last_score = -1
        for user, score in stats.items():
            if not last_score == score.points:
                index += 1
            if user.id == user_to_find.id:
                return index
            last_score = score.points

        return -1


    @staticmethod
    def markdown_presentation(new_stats: Dict[User, Score], old_stats: Dict[User, Score], time: int) -> str:
        if len(new_stats.keys()) == 0:
            return "Sadly there are no scores for event '" + str(time) + "'"
        text = "*Scoreboard for event:* " + str(time) + "\n\n`"

        index = 0
        last_score = -1
        for user, score in new_stats.items():
            if not last_score == score.points:
                index += 1
            if index == 1:
                text += "🥇  " + user.first_name
            elif index == 2:
                text += "🥈  " + user.first_name
            elif index == 3:
                text += "🥉  " + user.first_name
            else:
                text += " " + str(index) + ".  " + user.first_name

            text += " " * (10 - len(user.first_name))
            text += str(score.points) + " " * (3 - len(str(score.points)))

            if user in old_stats:
                text += "(+" + str(score.points - old_stats[user].points) + ") "
            else:
                text += "(+" + str(score.points) + ") "

            old_rank = StatisticService.get_statistic_rank(old_stats, user)
            if old_rank == index:
                text += "⏹"
            elif old_rank < index:
                text += "🔽"
            elif old_rank > index:
                text += "🔼"

            text += "\n"
            last_score = score.points

        return text + "`"

    @staticmethod
    def stats_to_time(time: int) -> str:
        statistic = StatisticRepo.get_or_create(time)

        # get old score for comparison
        unsorted_old_scores = StatisticService.extract_scores_from_statistic(statistic)
        sorted_old_scores = StatisticService.sort_dict(unsorted_old_scores)

        # calculate new scores
        StatisticService.calc_stats(statistic)
        unsorted_new_scores = StatisticService.extract_scores_from_statistic(statistic)
        sorted_new_scores = StatisticService.sort_dict(unsorted_new_scores)

        board_text = StatisticService.markdown_presentation(sorted_new_scores, sorted_old_scores, statistic.time)
        return board_text
