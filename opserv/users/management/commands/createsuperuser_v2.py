from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCommand,
)
from django.core.management import CommandError

from opserv.ranks.models import Rank
from opserv.users.models import User


class Command(BaseCommand):
    help = "Create a superuser and assign the default rank."

    def handle(self, *args, **options):
        super().handle(*args, **options)

        # Get the username from the options
        username = (
            options.get("username")
            or input("Enter the username of the superuser: ").strip()
        )
        if not username:
            message = "Username is required to assign the default rank."
            raise CommandError(message)

        # Fetch the created superuser
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            message = f"Superuser with username '{username}' does not exist."
            raise CommandError(message) from None

        # Assign the default rank to the superuser
        try:
            default_rank = Rank.objects.get(is_default=True)
            user.rank = default_rank
            self.stdout.write(
                self.style.SUCCESS(
                    f"Default rank '{default_rank.name}' assigned to superuser '{username}'.",  # noqa: E501
                ),
            )
        except Rank.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(
                    "No default rank found. Superuser created without a rank.",
                ),
            )
