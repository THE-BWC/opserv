from django.urls import path

from .views import rank_list

app_name = "ranks"
urlpatterns = [
    path("list/", view=rank_list, name="rank_list"),
]
