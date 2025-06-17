from http import HTTPStatus

import pytest
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from opserv.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestOperationsHomeView:
    def test_operations_home_view(self, client):
        response = client.get("/")
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == login_url

    def test_operations_home_view_authenticated(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get("/")

        assert response.status_code == HTTPStatus.OK
        assert "Welcome to the Operations Server" in str(response.content)
