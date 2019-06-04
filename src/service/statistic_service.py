from src.entity.score import Score
from src.entity.user import User
from src.entity.statistic import Statistic
from src.repo.score_repo import ScoreRepo
from src.repo.message_repo import MessageRepo
from src.repo.statistic_repo import StatisticRepo
import collections
from datetime import datetime

from typing import Dict


class StatisticService:

    @staticmethod
    def extract_scores(stat: Statistic) -> Dict[User, Score]:
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
            msg_date: int = int(msg.time.strftime('%Y%m%d'))
            msg_time: int = int(msg.time.strftime('%H%M'))
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

        # stat.last_msg_id = messages[-1].msg_id
        # StatisticRepo.save(stat)



    @staticmethod
    def html_presentation(stats: Dict[User, Score], time: int) -> str:
        if len(stats.keys()) == 0:
            return "Sadly there are no scores for event '" + str(time) + "'"
        text = "<b>Scoreboard for event: " + str(time) + "</b>\n\n"

        for user, score in stats.items():
            text += user.first_name + "  ---  " + str(score.points)

        return text
