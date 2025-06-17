from django.core.files.uploadedfile import SimpleUploadedFile
from factory import Faker
from factory.django import DjangoModelFactory

from opserv.games.models import Game


class GameFactory(DjangoModelFactory[Game]):
    name = Faker("name")
    tag = Faker("word")
    icon = SimpleUploadedFile("icon.png", b"file_content", content_type="image/png")

    class Meta:
        model = Game
        django_get_or_create = ["name", "tag"]
