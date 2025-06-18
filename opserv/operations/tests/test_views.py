from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse

from opserv.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestHomeView:
    def test_home_view_redirects_if_not_logged_in(self, client):
        response = client.get("/")
        login_url = reverse(settings.LOGIN_URL)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == login_url

    def test_home_view_renders_for_authenticated_user(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get("/")
        assert response.status_code == HTTPStatus.OK
        assert "home.html" in [t.name for t in response.templates]
        assert b"Welcome to the Operations Server" in response.content
        assert b"Upcoming Operations" in response.content

    def test_game_accordion_renders_games_and_operations(self, client):
        user = UserFactory()
        client.force_login(user)

        # Mock context: games with upcoming_operations
        games = [
            type(
                "Game",
                (),
                {
                    "id": 1,
                    "name": "Arma 3",
                    "icon": "arma3.png",
                    "upcoming_operations": [
                        type(
                            "Operation",
                            (),
                            {
                                "id": 101,
                                "name": "Operation Thunder",
                                "type_id": type(
                                    "Type",
                                    (),
                                    {
                                        "color_hex": "ff0000",
                                        "__str__": lambda self: "Co-op",
                                    },
                                )(),
                                "start_date": "2024-06-01T18:00:00Z",
                            },
                        )(),
                    ],
                },
            )(),
            type(
                "Game",
                (),
                {
                    "id": 2,
                    "name": "Squad",
                    "icon": "squad.png",
                    "upcoming_operations": [],
                },
            )(),
        ]

        with patch(
            "opserv.games.models.Game.objects.with_upcoming_operations",
            return_value=games,
        ):
            response = client.get("/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "Arma 3" in content
        assert "Operation Thunder" in content
        assert "Squad" in content

    def test_base_html_page_block_rendered(self, client, user):
        client.force_login(user)
        response = client.get("/")
        # Assert content from the 'page' block is present
        assert b"Welcome to the Operations Server" in response.content
