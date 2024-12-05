from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from admin_web.models import User, Admin, Dosen, Mahasiswa

class Command(BaseCommand):
    help = 'Seed User, Admin, Dosen, and Mahasiswa data'

    def handle(self, *args, **kwargs):
        password = make_password('password123')  # Hash password for all users

        for i in range(1, 151):  # Generate 150 mahasiswa
            email = f"mahasiswa{i:03d}@example.com"
            if not User.objects.filter(email=email).exists():
                mahasiswa_user = User.objects.create(
                    email=email,
                    role="mahasiswa",
                    is_active=True,
                    password=password
                )
                Mahasiswa.objects.create(
                    user=mahasiswa_user,  # Set user instance directly
                    nim=f"M{i:03d}",
                    nama=f"Mahasiswa User {i}",
                    email=email,
                    semester=(i % 8) + 1,  # Assign random semester between 1 and 8
                    mobile_phone=f"0812345678{i:03d}",
                    nik=f"3201234567890{i:04d}",
                    is_active=True,
                )
                self.stdout.write(self.style.SUCCESS(f"Mahasiswa '{email}' created."))
        self.stdout.write(self.style.SUCCESS('Seeding completed.'))
