import pytest
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from opserv.users.models import User
from opserv.ranks.models import Rank


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


@pytest.mark.django_db
def test_user_str(user: User):
    assert str(user) == user.username


@pytest.mark.django_db
def test_user_get_permissions(user: User):
    user_content_type = ContentType.objects.get_for_model(User)
    permission = Permission.objects.create(
        codename='test_permission',
        name='Test Permission',
        content_type=user_content_type
    )
    user.user_permissions.add(permission)

    assert user.has_perm('users.test_permission')
    assert not user.has_perm('users.non_existent_permission')
