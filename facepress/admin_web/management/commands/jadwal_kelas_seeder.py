# facepress/management/commands/jadwal_kelas_seeder.py

from django.core.management.base import BaseCommand
from admin_web.models import JadwalKelas, Kelas, MataKuliah, Ruang, Dosen
from datetime import timedelta, date, time

class Command(BaseCommand):
    help = 'Seed Jadwal Kelas data'

    def handle(self, *args, **kwargs):
        # Ambil semua kelas
        kelas_list = Kelas.objects.all()
        
        # Ambil semua dosen (atau sesuaikan sesuai kebutuhan)
        dosen_list = Dosen.objects.all()

        if not dosen_list.exists():
            self.stdout.write(self.style.ERROR("No Dosen found. Please seed Dosen data first."))
            return

        # Tentukan tanggal mulai
        start_date = date.today()  # Atau ganti dengan tanggal mulai yang diinginkan

        for kelas in kelas_list:
            for i in range(16):  # 16 pertemuan
                tanggal = start_date + timedelta(weeks=i)  # Tambah 1 minggu untuk setiap pertemuan
                jam_mulai = time(8 + (i % 3), 0)  # Contoh: Jam mulai 8, 9, dan 10
                jam_selesai = time(10 + (i % 3), 0)  # Jam selesai 2 jam setelah jam mulai
                status = "belum dimulai"  # Default status

                # Pilih dosen secara acak
                dosen = dosen_list.first()  # Menggunakan dosen pertama; Anda bisa menggantinya dengan logika yang lebih baik

                # Ambil mata kuliah untuk kelas
                mata_kuliah = kelas.mata_kuliah

                # Buat dan simpan jadwal
                jadwal = JadwalKelas(
                    tanggal=tanggal,
                    jam_mulai=jam_mulai,
                    jam_selesai=jam_selesai,
                    mata_kuliah=mata_kuliah,
                    kelas=kelas,
                    ruang=kelas.ruang,  # Gunakan ruang yang sama dengan kelas
                    dosen=dosen,
                    status=status
                )
                jadwal.save()
                self.stdout.write(self.style.SUCCESS(f"Created Jadwal: {jadwal}"))
