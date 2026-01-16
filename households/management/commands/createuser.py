from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from households.models import Household, HouseholdMembership


User = get_user_model()


class Command(BaseCommand):
    help = 'Create a new user and optionally add them to a household'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('password', type=str, help='Password for the new user')
        parser.add_argument(
            '--email',
            type=str,
            default='',
            help='Email address (optional)'
        )
        parser.add_argument(
            '--household',
            type=str,
            help='Household name to add user to (creates if does not exist)'
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Make user an ADMIN of the household (default is MEMBER)'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        household_name = options['household']
        is_admin = options['admin']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            raise CommandError(f'User "{username}" already exists')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        self.stdout.write(self.style.SUCCESS(f'Created user "{username}"'))

        # Add to household if specified
        if household_name:
            household, created = Household.objects.get_or_create(name=household_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created household "{household_name}"'))

            role = HouseholdMembership.Role.ADMIN if is_admin else HouseholdMembership.Role.MEMBER
            HouseholdMembership.objects.create(
                household=household,
                user=user,
                role=role
            )
            self.stdout.write(
                self.style.SUCCESS(f'Added "{username}" to "{household_name}" as {role}')
            )
