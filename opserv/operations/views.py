from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from opserv.games import models as games_models


@login_required
def home(request):
    """
    Home view that renders the home page.

    """
    # Fetch all games that have upcoming operations
    games = games_models.Game.objects.with_upcoming_operations()
    # Each game in games will have a `.upcoming_operations` attribute
    # (a list of upcoming operations)

    # If no games are found, return an empty list
    games = [] if not games else sorted(games, key=lambda game: game.name.lower())

    # Render the home page with the list of games
    return render(
        request,
        "home.html",
        {
            "games": games,
            "server_timezone": settings.TIME_ZONE,
            "current_path": request.path,
        },
    )
