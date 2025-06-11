from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import PROTECT
from django.db.models import CharField
from django.db.models import ForeignKey
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_default_rank_id() -> int | None:
    """Get the default rank ID.

    Returns:
        int: Default rank ID, or None if not found.

    """
    from opserv.ranks.models import Rank

    try:
        return Rank.objects.get(is_default=True).id
    except ObjectDoesNotExist:
        return None


class User(AbstractUser):
    """
    Default custom user model for OpServ.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    rank = ForeignKey(
        "ranks.Rank",
        verbose_name=_("Rank"),
        on_delete=PROTECT,
        related_name="user_set",
        default=get_default_rank_id,
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
