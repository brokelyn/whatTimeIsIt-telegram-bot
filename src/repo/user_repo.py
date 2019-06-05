from entity.user import User


class UserRepo:

    @staticmethod
    def create(user: User):
        user.save(force_insert=True)

    @staticmethod
    def save(user: User):
        user.save()

    @staticmethod
    def create_if_not_exist(user: User):
        query = User.select().where(User.id == user.id)
        if not query.exists():
            UserRepo.create(user)

    @staticmethod
    def get_or_none(id: int) -> User:
        return User.get_or_none(User.id == id)
