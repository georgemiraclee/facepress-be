# facepress/management/commands/ruang_seeder.py

from django.core.management.base import BaseCommand
from admin_web.models import Ruang

class Command(BaseCommand):
    help = 'Seed Ruang data'

    def handle(self, *args, **kwargs):
        ruang_data = [
            {"nama_ruang": "A201", "lokasi": "Gedung Baru"},
            {"nama_ruang": "A202", "lokasi": "Gedung Baru"},
            {"nama_ruang": "Lab PJK", "lokasi": "Gedung Baru"},
            {"nama_ruang": "Lab Multimedia", "lokasi": "Gedung Baru"},
            {"nama_ruang": "Lab TKO", "lokasi": "Gedung Baru"},
            {"nama_ruang": "Lab Jaringan", "lokasi": "Gedung Baru"},
            {"nama_ruang": "B201", "lokasi": "Gedung Lama"},
            {"nama_ruang": "B202", "lokasi": "Gedung Lama"},
            {"nama_ruang": "RBC", "lokasi": "Gedung Lama"}
        ]

        for ruang in ruang_data:
            Ruang.objects.create(nama_ruang=ruang["nama_ruang"], lokasi=ruang["lokasi"])
            self.stdout.write(self.style.SUCCESS(f"Created Ruang: {ruang['nama_ruang']} - {ruang['lokasi']}"))
