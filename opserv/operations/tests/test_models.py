from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from opserv.operations.models import Operation
from opserv.operations.models import OperationType


@pytest.mark.django_db
def test_operation_type_str():
    operation_type = OperationType.objects.create(
        id=1,
        name="Test Operation Type",
    )

    assert str(operation_type) == "Test Operation Type"


@pytest.mark.django_db
def test_operation_str():
    from opserv.games.models import Game

    # Ensure the Game exists
    game = Game.objects.create(
        name="Test Game",
        tag="TG",
        icon="games/test.png",
    )

    # Ensure the OperationType exists
    operation_type = OperationType.objects.create(
        id=1,
        name="Test Operation Type",
    )

    # Create a user to associate with the operation
    user_model = get_user_model()
    user = user_model.objects.create(username="testuser")

    operation = Operation.objects.create(
        name="Test Operation",
        game_id=game,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=1),
        type_id=operation_type,
        leader_user_id=user,
    )

    assert str(operation) == "Test Operation"
