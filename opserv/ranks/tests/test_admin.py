import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from opserv.ranks.admin import RankAdmin
from opserv.ranks.models import Rank

User = get_user_model()


@pytest.fixture
def rank_with_users(db):
    user1 = User.objects.create(username="user1")
    user2 = User.objects.create(username="user2")
    rank = Rank.objects.create(
        name="Sergeant",
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )
    rank.users.add(user1, user2)
    return rank, [user1, user2]


@pytest.fixture
def rank_without_users(db):
    return Rank.objects.create(
        name="Private",
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )


def test_users_display_with_users(rank_with_users):
    rank, users = rank_with_users
    admin = RankAdmin(Rank, AdminSite())
    result = admin.users_display(rank)
    assert users[0].username in result
    assert users[1].username in result


def test_users_display_without_users(rank_without_users):
    admin = RankAdmin(Rank, AdminSite())
    result = admin.users_display(rank_without_users)
    assert result == "No users assigned"


def test_is_default_display_true(db):
    rank = Rank.objects.create(
        name="Default",
        is_default=True,
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )
    admin = RankAdmin(Rank, AdminSite())
    assert admin.is_default_display(rank) is True


def test_is_default_display_false(db):
    rank = Rank.objects.create(
        name="NotDefault",
        is_default=False,
        icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
        fs_icon=SimpleUploadedFile("fs_icon.png", b"fsicon", content_type="image/png"),
    )
    admin = RankAdmin(Rank, AdminSite())
    assert admin.is_default_display(rank) is False
