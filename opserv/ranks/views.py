from django.conf import settings
from django.shortcuts import render

from .models import Rank


def rank_list(request):
    """
    Renders a list of ranks.
    """
    ranks = Rank.objects.all()
    context = {
        "ranks": ranks,
        "static_url": settings.STATIC_URL,
        "current_path": request.path,
    }
    return render(request, "ranks/rank_list.html", context)
