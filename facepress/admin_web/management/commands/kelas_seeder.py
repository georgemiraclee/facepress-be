# facepress/management/commands/kelas_seeder.py

from django.core.management.base import BaseCommand
from admin_web.models import Kelas, MataKuliah, Ruang
from datetime import time

class Command(BaseCommand):
    help = 'Seed kelas data'

    def handle(self, *args, **kwargs):
        mata_kuliah_list = MataKuliah.objects.all()
        ruang_list = Ruang.objects.all()

        if not ruang_list.exists():
            self.stdout.write(self.style.ERROR("No Ruang found. Please seed Ruang data first."))
            return
        
        for mata_kuliah in mata_kuliah_list:
            for suffix in ['A', 'B', 'C', 'D']:
                nama_kelas = f"Kelas {suffix}"
                kode_kelas = f"{mata_kuliah.kode}-{suffix}"
                
                ruang = ruang_list.first() 
                
                kelas = Kelas(
                    nama_kelas=nama_kelas,
                    kode_kelas=kode_kelas,
                    mata_kuliah=mata_kuliah,
                    ruang=ruang,
                    hari="Senin", 
                    jam_mulai=time(8, 0),
                    jam_selesai=time(10, 0),
                    kapasitas=30 
                )
                kelas.save()
                self.stdout.write(self.style.SUCCESS(f"Created kelas: {nama_kelas} for mata kuliah: {mata_kuliah.nama}"))
