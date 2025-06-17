from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import PROTECT
from django.db.models import CharField
from django.db.models import ForeignKey
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from opserv.ranks.models import Rank


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
        Rank,
        on_delete=PROTECT,
        related_name="users",
        verbose_name=_("Rank"),
        default=1,  # Default to the first rank
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def has_perm(self, perm, obj=None):
        # Check default permissions
        if super().has_perm(perm, obj):
            return True

        # Check rank permissions
        if self.rank and perm in self.rank.permissions.values_list(
            "codename",
            flat=True,
        ):
            return True

        # Check billet permissions
        try:
            if self.billet and perm in self.billet.permissions.values_list(
                "codename",
                flat=True,
            ):
                return True
        except ObjectDoesNotExist:
            pass

        return False
