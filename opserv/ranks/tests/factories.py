from django.core.files.uploadedfile import SimpleUploadedFile
from factory import Faker
from factory.django import DjangoModelFactory

from opserv.ranks.models import Rank


class RankFactory(DjangoModelFactory[Rank]):
    name = Faker("name")
    icon = SimpleUploadedFile("icon.png", b"file_content", content_type="image/png")
    fs_icon = SimpleUploadedFile("icon.png", b"file_content", content_type="image/png")

    class Meta:
        model = Rank
        django_get_or_create = ["name"]
