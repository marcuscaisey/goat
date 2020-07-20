import factory

from lists.models import Item, List
from users.models import User


class ListFactory(factory.DjangoModelFactory):
    class Meta:
        model = List


class ItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = Item

    text = factory.sequence(lambda n: f"list item {n + 1}")
    list = factory.SubFactory(ListFactory)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.Faker("password")

    @factory.post_generation
    def hash_password(obj, create, extracted, **kwargs):
        obj.set_password(obj.password)
