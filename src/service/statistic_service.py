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
        messages = MessageRepo.findByStatistic(stat)

        if len(messages) == 0:
            return

        user_score_dict = StatisticService.extract_scores_from_statistic(stat)

        # Group messages by day
        messages_by_day = {}
        for msg in messages:
            time_tz = TimeService.datetime_correct_tz(msg.time, stat.group.timezone)
            msg_date: int = int(time_tz.strftime('%Y%m%d'))
            msg_time: int = int(time_tz.strftime('%H%M'))

            # Only process valid messages
            if msg_time == stat.time and pattern in msg.text:
                if msg_date not in messages_by_day:
                    messages_by_day[msg_date] = []
                messages_by_day[msg_date].append(msg)

        # Process each day
        for day in sorted(messages_by_day.keys()):
            daily_messages = messages_by_day[day]
            users_who_posted_today = []

            # Award 1 point to each user who posted correctly on this day
            for msg in daily_messages:
                user = msg.user

                # Initialize score if user doesn't exist
                if user not in user_score_dict:
                    new_score = Score(user=user, stat=stat, points=0, date=0)
                    user_score_dict[user] = new_score

                # Only award point if this is a new day for this user
                if day > user_score_dict[user].date and user not in users_who_posted_today:
                    user_score_dict[user].points += 1
                    user_score_dict[user].date = day

                    # Track that this user posted today (only count once per user)
                    if user not in users_who_posted_today:
                        users_who_posted_today.append(user)

            # Award bonus points for this day
            if len(users_who_posted_today) == 1:
                # Solo player gets +1 bonus (2 points total for the day)
                user_score_dict[users_who_posted_today[0]].points += 1
            elif len(users_who_posted_today) > 1:
                # First player gets +1 bonus when multiple players posted
                user_score_dict[users_who_posted_today[0]].points += 1

        # Save all scores
        for score in user_score_dict.values():
            ScoreRepo.save(score)

        # Update the last processed message ID
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
            return "There are no scores for time '" + str(time) + "'"
        text = "*Scoreboard for time   *" + str(time) + "\n\n`"

        index = 0
        last_score = -1
        for user, score in new_stats.items():
            if not last_score == score.points:
                index += 1
            if index == 1:
                text += "🥇 " + user.first_name
            elif index == 2:
                text += "🥈 " + user.first_name
            elif index == 3:
                text += "🥉 " + user.first_name
            else:
                text += str(index) + ". " + user.first_name

            text += " " * (10 - len(user.first_name))
            text += str(score.points) + " " * (3 - len(str(score.points)))

            if user in old_stats:
                text += "(+" + str(score.points - old_stats[user].points) + ") "
            else:
                text += "(+" + str(score.points) + ") "

            old_rank = StatisticService.get_statistic_rank(old_stats, user)
            if old_rank == index:
                text += "⏹"
            elif old_rank > index or old_rank == -1:
                text += "🔼"
            elif old_rank < index:
                text += "🔽"

            text += "\n"
            last_score = score.points

        return text + "`"

    @staticmethod
    def stats_to_time(group_id: int, time: int) -> str:
        statistic = StatisticRepo.get_or_create(group_id, time)

        # get old score for comparison
        unsorted_old_scores = StatisticService.extract_scores_from_statistic(statistic)
        sorted_old_scores = StatisticService.sort_dict(unsorted_old_scores)

        # calculate new scores
        StatisticService.calc_stats(statistic)
        unsorted_new_scores = StatisticService.extract_scores_from_statistic(statistic)
        sorted_new_scores = StatisticService.sort_dict(unsorted_new_scores)

        board_text = StatisticService.markdown_presentation(sorted_new_scores, sorted_old_scores, statistic.time)
        return board_text
