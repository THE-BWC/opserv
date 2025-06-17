from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from opserv.billets.models import Billet
from opserv.billets.models import BilletOffice
from opserv.games.tests.factories import GameFactory
from opserv.ranks.tests.factories import RankFactory
from opserv.users.tests.factories import UserFactory


class BilletOfficeFactory(DjangoModelFactory[BilletOffice]):
    office_name = Faker("name")

    class Meta:
        model = BilletOffice
        django_get_or_create = ["office_name"]


class BilletFactory(DjangoModelFactory[Billet]):
    name = Faker("name")
    description = Faker("text")
    office = SubFactory(BilletOfficeFactory)
    game = SubFactory(GameFactory)
    rank = SubFactory(RankFactory)

    created_by = SubFactory(UserFactory)
    updated_by = SubFactory(UserFactory)

    class Meta:
        model = Billet
        django_get_or_create = ["name", "office", "game", "rank"]
