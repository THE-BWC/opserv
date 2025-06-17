import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from opserv.billets import admin as my_admin
from opserv.billets.models import Billet
from opserv.billets.models import BilletOffice
from opserv.games.models import Game
from opserv.ranks.models import Rank


@pytest.mark.django_db
def test_billet_registered_with_admin():
    assert admin.site.is_registered(Billet)


@pytest.mark.django_db
def test_billet_office_registered_with_admin():
    assert admin.site.is_registered(BilletOffice)


@pytest.mark.django_db
def test_billet_admin_get_readonly_fields():
    billet_admin = my_admin.BilletAdmin(Billet, admin.site)
    request = RequestFactory().get("/")
    readonly_fields = billet_admin.get_readonly_fields(request)
    assert {"created_by", "updated_by", "created_at", "updated_at"}.issubset(
        readonly_fields,
    )


@pytest.mark.django_db
def test_billet_admin_get_fields_create_and_change():
    billet_admin = my_admin.BilletAdmin(Billet, admin.site)
    request = RequestFactory().get("/")
    user_model = get_user_model()
    user1 = user_model.objects.create(username="testuser")
    request.user = user1
    # On create (obj=None), created_by and updated_by should not be in fields
    fields_create = billet_admin.get_fields(request, obj=None)
    assert "created_by" not in fields_create
    assert "updated_by" not in fields_create
    # On change (obj exists), fields should include created_by and updated_by
    billet = Billet()
    fields_change = billet_admin.get_fields(request, obj=billet)
    assert "created_by" in fields_change
    assert "updated_by" in fields_change


@pytest.mark.django_db
def test_billet_admin_save_model_sets_users():
    billet_admin = my_admin.BilletAdmin(Billet, admin.site)
    request = RequestFactory().post("/")
    user_model = get_user_model()
    user1 = user_model.objects.create(username="testuser")
    request.user = user1

    # Create a BilletOffice instance
    office = BilletOffice.objects.create(office_name="Test Office")

    # Create a Game and Rank instance
    game = Game.objects.create(name="Test Game")
    office.game = game
    office.save()

    rank = Rank.objects.create(name="Test Rank")

    # On create, created_by and updated_by should be set to the request user
    billet = Billet(name="Test Billet", office=office, game=game, rank=rank)
    billet_admin.save_model(request, billet, None, change=False)
    assert billet.created_by == user1
    assert billet.updated_by == user1

    # On update, only updated_by should change
    user2 = user_model.objects.create(username="updateuser")
    request.user = user2
    billet_admin.save_model(request, billet, None, change=True)
    assert billet.created_by == user1
    assert billet.updated_by == user2
