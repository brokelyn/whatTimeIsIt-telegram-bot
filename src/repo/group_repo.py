from entity.group import Group


class GroupRepo:

    @staticmethod
    def create(group: Group):
        group.save(force_insert=True)

    @staticmethod
    def save(group: Group):
        group.save()

    @staticmethod
    def create_if_not_exist(group: Group):
        query = Group.select().where(Group.id == group.id)
        if not query.exists():
            GroupRepo.create(group)

    @staticmethod
    def get_or_create(id: int, title: str) -> Group:
        group = Group.get_or_none(Group.id == id)
        if group is not None:
            return group
        else:
            group = Group(id=id, title=title)
            GroupRepo.create(group)
            return group

    @staticmethod
    def get_or_none(id: int) -> Group:
        return Group.get_or_none(Group.id == id)

    @staticmethod
    def findAll():
        return list(Group.select())
