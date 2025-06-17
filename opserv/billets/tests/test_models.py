import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from opserv.billets.models import Billet
from opserv.billets.models import BilletOffice
from opserv.games.models import Game
from opserv.ranks.models import Rank


@pytest.mark.django_db
def test_billet_office_str():
    office = BilletOffice.objects.create(office_name="HQ")
    assert str(office) == "HQ"
    office.office_name = ""
    office.save()
    assert str(office) == "Unnamed Office"


@pytest.mark.django_db
def test_billet_str():
    user = get_user_model().objects.create(username="creator")
    office = BilletOffice.objects.create(office_name="HQ")
    game = Game.objects.create(name="Test Game")
    rank = Rank.objects.create(name="Test Rank")
    billet = Billet.objects.create(
        name="Commander",
        office=office,
        game=game,
        rank=rank,
        created_by=user,
        updated_by=user,
    )
    assert str(billet) == "Commander"
    billet.name = ""
    billet.save()
    assert str(billet) == "Unnamed Billet"


@pytest.mark.django_db
def test_billet_save_sets_created_by_and_updated_by():
    user = get_user_model().objects.create(username="creator")
    office = BilletOffice.objects.create(office_name="HQ")
    game = Game.objects.create(name="Test Game")
    rank = Rank.objects.create(name="Test Rank")
    request = RequestFactory().post("/")
    request.user = user

    billet = Billet(
        name="Commander",
        office=office,
        game=game,
        rank=rank,
        created_by=user,
        updated_by=user,
    )
    billet.save(request=request)
    assert billet.created_by == user
    assert billet.updated_by == user

    # On update, only updated_by should change
    user2 = get_user_model().objects.create(username="updater")
    request.user = user2
    billet.save(request=request)
    assert billet.created_by == user
    assert billet.updated_by == user2
