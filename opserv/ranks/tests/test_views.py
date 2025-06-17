from http import HTTPStatus

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.urls import reverse

from opserv.ranks.models import Rank
from opserv.ranks.views import rank_list
from opserv.users.models import User

pytestmark = pytest.mark.django_db


class TestRankListView:
    def test_rank_list_view_status_code(self, user: User, rf: RequestFactory):
        request = rf.get(reverse("ranks:rank_list"))
        request.user = user
        response = rank_list(request)
        assert response.status_code == HTTPStatus.OK

    def test_rank_list_view_template_used(self, user: User, client):
        client.force_login(user)
        response = client.get(reverse("ranks:rank_list"))
        assert response.status_code == HTTPStatus.OK
        assert "ranks/rank_list.html" in [t.name for t in response.templates]


class TestRankListViewContext:
    def test_rank_list_view_context_contains_ranks(self, user: User, client):
        rank = Rank.objects.create(
            name="Sergeant",
            icon=SimpleUploadedFile("icon.png", b"icon", content_type="image/png"),
            fs_icon=SimpleUploadedFile(
                "fs_icon.png",
                b"fsicon",
                content_type="image/png",
            ),
        )
        client.force_login(user)
        response = client.get(reverse("ranks:rank_list"))

        assert response.status_code == HTTPStatus.OK
        assert "ranks" in response.context
        assert rank in response.context["ranks"]
