from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
from django.urls import reverse

EXEMPT_URLS = [
    reverse(settings.LOGIN_URL),
    "/admin/",
    "/static/",
    "/api/",
    "/accounts/confirm-email/",
    "/accounts/discord/",
]
EXEMPT_VIEWS = ["account_login", "account_logout", "account_signup"]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            resolved_view = resolve(path).view_name
            if (
                not any(path.startswith(url) for url in EXEMPT_URLS)
                and resolved_view not in EXEMPT_VIEWS
            ):
                return redirect(reverse(settings.LOGIN_URL))
        return self.get_response(request)
