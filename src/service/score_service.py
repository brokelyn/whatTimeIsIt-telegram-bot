from src.entity.event import Event
from src.entity.score import Score
from src.entity.user import User
from src.repo.score_repo import ScoreRepo


class ScoreService:

    @staticmethod
    def increase_score(event: Event, user: User):
        score = ScoreRepo.get_score(event, user)
        if score:
            score.points += 1
        else:
            score = ScoreService.create_score(event, user)
            score.points = 1
            ScoreRepo.save(score)

    @staticmethod
    def create_score(event: Event, user: User):
        score = ScoreRepo.get_score(event, user)
        if score:
            score = Score(user=user, event=event)
            ScoreRepo.save(score)
        return score
