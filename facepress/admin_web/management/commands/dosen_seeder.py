from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from admin_web.models import User, Admin, Dosen, Mahasiswa

class Command(BaseCommand):
    help = 'Seed User, Admin, Dosen, and Mahasiswa data'

    def handle(self, *args, **kwargs):
        password = make_password('password123')  # Hash password for all users
        for i in range(1, 16):  # Generate 15 dosen
            email = f"dosen{i:02d}@example.com"
            if not User.objects.filter(email=email).exists():
                dosen_user = User.objects.create(
                    email=email,
                    role="dosen",
                    is_active=True,
                    password=password
                )
                Dosen.objects.create(
                    user=dosen_user,  # Set user instance directly
                    nip=f"D{i:03d}",
                    nama=f"Dosen User {i}",
                    email=email,
                    mobile_phone=f"0812345678{i:03d}",                    
                )
                self.stdout.write(self.style.SUCCESS(f"Dosen '{email}' created."))
            
        self.stdout.write(self.style.SUCCESS('Seeding completed.'))
