import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from opserv.billets.tests.factories import BilletFactory
from opserv.ranks.models import Rank
from opserv.users.models import User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


@pytest.mark.django_db
def test_user_str(user: User):
    assert str(user) == user.username


@pytest.mark.django_db
def test_user_get_permissions(user: User):
    user_content_type = ContentType.objects.get_for_model(User)
    permission = Permission.objects.create(
        codename="test_permission",
        name="Test Permission",
        content_type=user_content_type,
    )
    user.user_permissions.add(permission)

    assert user.has_perm("users.test_permission")
    assert not user.has_perm("users.non_existent_permission")


@pytest.mark.django_db
def test_user_get_permissions_no_permissions(user: User):
    assert not user.has_perm("users.test_permission")
    assert not user.has_perm("users.non_existent_permission")


@pytest.mark.django_db
def test_user_get_rank_permissions(user: User):
    user_content_type = ContentType.objects.get_for_model(User)
    permission = Permission.objects.create(
        codename="test_rank_permission",
        name="Test Rank Permission",
        content_type=user_content_type,
    )
    rank = Rank.objects.create(
        name="Test Rank",
        description="This is a test rank.",
    )
    rank.permissions.add(permission)
    user.rank = rank
    user.save()

    assert user.has_perm("test_rank_permission")
    assert not user.has_perm("non_existent_permission")


@pytest.mark.django_db
def test_user_get_billet_permissions(user: User):
    user_content_type = ContentType.objects.get_for_model(User)
    permission = Permission.objects.create(
        codename="test_billet_permission",
        name="Test Billet Permission",
        content_type=user_content_type,
    )

    billet = BilletFactory()

    billet.permissions.add(permission)
    user.billet = billet
    user.save()

    assert user.has_perm("test_billet_permission")
    assert not user.has_perm("non_existent_billet_permission")
