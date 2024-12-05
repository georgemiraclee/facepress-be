from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from admin_web.models import User, Admin, Dosen, Mahasiswa

class Command(BaseCommand):
    help = 'Seed User, Admin, Dosen, and Mahasiswa data'

    def handle(self, *args, **kwargs):
        password = make_password('password123')  # Hash password for all users

        # Seed Admin data (1 Admin)
        if not User.objects.filter(email="admin@example.com").exists():
            admin_user = User.objects.create(
                email="admin@example.com",
                role="admin",
                is_active=True,
                is_superuser=True,
                password=password
            )
            Admin.objects.create(
                user=admin_user,  # Set user instance directly
                nip="A001",
                name="Admin User",
                email="admin@example.com",
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Admin 'admin@example.com' created."))
        
        self.stdout.write(self.style.SUCCESS('Seeding completed.'))