from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Game


@pytest.mark.django_db
def test_game_str():
    game = Game.objects.create(
        name="Test Game",
        tag="TG",
        icon="games/test.png",
    )
    assert str(game) == "Test Game"


@pytest.mark.django_db
def test_with_upcoming_operations_returns_games_with_future_ops():
    from opserv.operations.models import Operation
    from opserv.operations.models import OperationType

    game_with_op = Game.objects.create(
        name="Game With Op",
        tag="GWO",
        icon="games/gwo.png",
    )
    game_without_op = Game.objects.create(
        name="Game Without Op",
        tag="GWOUT",
        icon="games/gwout.png",
    )

    # Ensure the OperationType exists
    operation_type = OperationType.objects.create(
        id=1,
        name="Test Operation Type",
    )

    # Create a user to associate with the operation
    user_model = get_user_model()
    user = user_model.objects.create(username="testuser")

    # Create a future operation for game_with_op
    Operation.objects.create(
        game_id=game_with_op,
        start_date=timezone.now() + timedelta(days=1),
        end_date=timezone.now() + timedelta(days=2),
        type_id=operation_type,
        leader_user_id=user,
    )
    # No operation for game_without_op

    games = Game.objects.with_upcoming_operations()
    assert game_with_op in games
    assert game_without_op not in games
