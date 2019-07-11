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

        name_score = dict()
        for score in scores:
            name_score[score.user] = score

        return name_score

    @staticmethod
    def sort_dict(stats: Dict[User, int]) -> Dict[User, int]:
        sorted_x = sorted(stats.items(), key=lambda kv: kv[1])
        sorted_x.reverse()
        return collections.OrderedDict(sorted_x)

    @staticmethod
    def calc_stats(stat: Statistic):
        pattern = str(stat.time)
        scores = ScoreRepo.scores_to_stat(stat)
        messages = MessageRepo.findByMsgIdIsGreater(stat.last_msg_id)
        if len(messages) == 0:
            return

        user_score_dict = dict()

        for score in scores:
            user_score_dict[score.user] = score

        for msg in messages:
            time_tz = TimeService.datetime_apply_tz(msg.time)
            msg_date: int = int(time_tz.strftime('%Y%m%d'))
            msg_time: int = int(time_tz.strftime('%H%M'))
            if msg_time == stat.time:
                if pattern in msg.text:
                    if msg.user not in user_score_dict:
                        score = Score(user=msg.user, stat=stat)
                        user_score_dict[msg.user] = score
                    if msg_date != user_score_dict[msg.user].date:
                        user_score_dict[msg.user].points += 1
                        user_score_dict[msg.user].date = msg_date

        # save the new scores and stats
        for score in user_score_dict.values():
            ScoreRepo.save(score)

        stat.last_msg_id = messages[-1].msg_id
        StatisticRepo.save(stat)



    @staticmethod
    def markdown_presentation(stats: Dict[User, Score], time: int) -> str:
        if len(stats.keys()) == 0:
            return "Sadly there are no scores for event '" + str(time) + "'"
        text = "*Scoreboard for event:* " + str(time) + "\n\n`"

        index = 1
        for user, score in stats.items():
            text += str(index) + ". " + user.first_name
            text += " " * (17 - len(user.first_name))
            text += str(score.points) + "\n"
            index += 1

        return text + "`"

    @staticmethod
    def stats_to_time(time: int) -> str:
        statistic = StatisticRepo.get_or_create(time)
        StatisticService.calc_stats(statistic)
        unsorted_dict = StatisticService.extract_scores_from_statistic(statistic)
        sorted_dict = StatisticService.sort_dict(unsorted_dict)
        board_text = StatisticService.markdown_presentation(sorted_dict, statistic.time)
        return board_text
