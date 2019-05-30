from src.entity.user import User


class UserRepo:

    @staticmethod
    def save(user: User):
        user.save()
