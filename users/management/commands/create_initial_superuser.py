"""
Custom management command to create a superuser programmatically.

Usage:
    python manage.py create_initial_superuser
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Create an initial superuser if one does not exist'

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists. Skipping creation.')
            )
            return
        
        # Get credentials from environment variables
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        # Validate password length
        if len(password) < 8:
            raise CommandError('Password must be at least 8 characters long.')
        
        try:
            # Create superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ Superuser created successfully!\n'
                    f'  Username: {username}\n'
                    f'  Email: {email}\n'
                    f'  Password: {password}\n\n'
                    f'  Please change the password after first login!\n'
                    f'  Access admin at: /admin/\n'
                )
            )
        except Exception as e:
            raise CommandError(f'Error creating superuser: {e}')
