from src.entity.user import User


class UserRepo:

    @staticmethod
    def save(user: User):
        user.save(force_insert=True)

    @staticmethod
    def save_if_not_exist(user: User):
        query = User.select().where(User.username == user.username)
        if not query.exists():
            UserRepo.save(user)
