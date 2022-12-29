"""Define factories to generate testing data."""
from factory import Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from ..models import MyModel


class MyFactory(DjangoModelFactory):

    field1 = Faker("sentence")

    class Meta:
        model = MyModel
