import factory

from lists.models import Item, List


class ListFactory(factory.DjangoModelFactory):
    class Meta:
        model = List


class ItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = Item

    text = factory.sequence(lambda n: f"list item {n + 1}")
    list = factory.SubFactory(ListFactory)
