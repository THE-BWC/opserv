import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from opserv.ranks.models import Rank


@pytest.mark.django_db
def test_rank_creation():
    rank = Rank.objects.create(
        name="Sergeant",
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )
    assert rank.pk is not None
    assert rank.name == "Sergeant"


@pytest.mark.django_db
def test_rank_str():
    rank = Rank.objects.create(
        name="Captain",
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )
    assert str(rank) == "Captain"


@pytest.mark.django_db
def test_color_hex_normalization():
    rank = Rank.objects.create(
        name="Lieutenant",
        color_hex="123456",
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )
    assert rank.color_hex == "#123456"


@pytest.mark.django_db
def test_only_one_default_rank():
    r1 = Rank.objects.create(
        name="Default1",
        is_default=True,
        icon=SimpleUploadedFile("icon1.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon1.png", b"fsicon", content_type="image/png"),
    )
    r2 = Rank.objects.create(
        name="Default2",
        is_default=True,
        icon=SimpleUploadedFile("icon2.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon2.png", b"fsicon", content_type="image/png"),
    )
    r1.refresh_from_db()
    r2.refresh_from_db()
    assert r1.is_default is False
    assert r2.is_default is True
