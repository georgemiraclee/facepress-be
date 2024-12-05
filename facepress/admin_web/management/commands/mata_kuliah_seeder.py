# facepress/management/commands/mata_kuliah_seeder.py

from django.core.management.base import BaseCommand
from admin_web.models import MataKuliah, Dosen
from admin_web.mata_kuliah.serializers import MataKuliahSerializer

class Command(BaseCommand):
    help = 'Seed mata kuliah data'

    def handle(self, *args, **kwargs):
        # Data dummy untuk mata kuliah
        mata_kuliah_data = [
            {
                "nama": "Algoritma dan Struktur Data",
                "nama_english": "Algorithms and Data Structures",
                "kode": "CS101",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 1,
                "status": "aktif",
                "dosen_ids": [3, 4]
            },
            {
                "nama": "Pemrograman Dasar",
                "nama_english": "Basic Programming",
                "kode": "CS102",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 1,
                "status": "aktif",
                "dosen_ids": [5, 6]
            },
            {
                "nama": "Basis Data",
                "nama_english": "Database",
                "kode": "CS103",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 2,
                "status": "aktif",
                "dosen_ids": [3, 5]
            },
            {
                "nama": "Rekayasa Perangkat Lunak",
                "nama_english": "Software Engineering",
                "kode": "CS104",
                "tipe": "Wajib",
                "sks": 4,
                "semester": 3,
                "status": "aktif",
                "dosen_ids": [6, 7]
            },
            {
                "nama": "Jaringan Komputer",
                "nama_english": "Computer Networks",
                "kode": "CS105",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 4,
                "status": "aktif",
                "dosen_ids": [3, 4]
            },
            {
                "nama": "Sistem Operasi",
                "nama_english": "Operating Systems",
                "kode": "CS106",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 4,
                "status": "aktif",
                "dosen_ids": [5, 8]
            },
            {
                "nama": "Kecerdasan Buatan",
                "nama_english": "Artificial Intelligence",
                "kode": "CS107",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [6, 9]
            },
            {
                "nama": "Pemrograman Web",
                "nama_english": "Web Programming",
                "kode": "CS108",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 3,
                "status": "aktif",
                "dosen_ids": [4, 10]
            },
            {
                "nama": "Pengolahan Citra",
                "nama_english": "Image Processing",
                "kode": "CS109",
                "tipe": "Pilihan",
                "sks": 3,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [3, 11]
            },
            {
                "nama": "Analisis Algoritma",
                "nama_english": "Algorithm Analysis",
                "kode": "CS110",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [5, 7]
            },
            {
                "nama": "Statistika",
                "nama_english": "Statistics",
                "kode": "CS111",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 2,
                "status": "aktif",
                "dosen_ids": [4, 6]
            },
            {
                "nama": "Sistem Terdistribusi",
                "nama_english": "Distributed Systems",
                "kode": "CS112",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 7,
                "status": "aktif",
                "dosen_ids": [8, 9]
            },
            {
                "nama": "Teknologi Web",
                "nama_english": "Web Technology",
                "kode": "CS113",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [10, 11]
            },
            {
                "nama": "Sistem Informasi",
                "nama_english": "Information Systems",
                "kode": "CS114",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 2,
                "status": "aktif",
                "dosen_ids": [3, 5]
            },
            {
                "nama": "Machine Learning",
                "nama_english": "Machine Learning",
                "kode": "CS115",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [6, 9]
            },
            {
                "nama": "Keamanan Jaringan",
                "nama_english": "Network Security",
                "kode": "CS116",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 7,
                "status": "aktif",
                "dosen_ids": [4, 8]
            },
            {
                "nama": "Pengembangan Aplikasi Mobile",
                "nama_english": "Mobile Application Development",
                "kode": "CS117",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [5, 10]
            },
            {
                "nama": "Pemrograman Lanjut",
                "nama_english": "Advanced Programming",
                "kode": "CS118",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 4,
                "status": "aktif",
                "dosen_ids": [3, 7]
            },
            {
                "nama": "Interaksi Manusia dan Komputer",
                "nama_english": "Human-Computer Interaction",
                "kode": "CS119",
                "tipe": "Pilihan",
                "sks": 3,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [6, 11]
            },
            {
                "nama": "Kalkulus",
                "nama_english": "Calculus",
                "kode": "MATH101",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 1,
                "status": "aktif",
                "dosen_ids": [5, 9]
            },
            {
                "nama": "Aljabar Linear",
                "nama_english": "Linear Algebra",
                "kode": "MATH102",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 2,
                "status": "aktif",
                "dosen_ids": [6, 8]
            },
            {
                "nama": "Statistika Dasar",
                "nama_english": "Basic Statistics",
                "kode": "MATH103",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 3,
                "status": "aktif",
                "dosen_ids": [4, 10]
            },
            {
                "nama": "Matematika Diskrit",
                "nama_english": "Discrete Mathematics",
                "kode": "MATH104",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 4,
                "status": "aktif",
                "dosen_ids": [3, 5]
            },
            {
                "nama": "Pemrograman Berorientasi Objek",
                "nama_english": "Object-Oriented Programming",
                "kode": "CS120",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [7, 9]
            },
            {
                "nama": "Sistem Multimedia",
                "nama_english": "Multimedia Systems",
                "kode": "CS121",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [10, 11]
            },
            {
                "nama": "Pengembangan Web Dinamis",
                "nama_english": "Dynamic Web Development",
                "kode": "CS122",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 4,
                "status": "aktif",
                "dosen_ids": [3, 5]
            },
            {
                "nama": "Teknik Kompilasi",
                "nama_english": "Compiler Techniques",
                "kode": "CS123",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 7,
                "status": "aktif",
                "dosen_ids": [6, 9]
            },
            {
                "nama": "Pengembangan Sistem Informasi",
                "nama_english": "Information System Development",
                "kode": "CS124",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [5, 8]
            },
            {
                "nama": "Pengujian Perangkat Lunak",
                "nama_english": "Software Testing",
                "kode": "CS125",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [7, 11]
            },
            {
                "nama": "Sistem Informasi Geografis",
                "nama_english": "Geographic Information Systems",
                "kode": "CS126",
                "tipe": "Pilihan",
                "sks": 3,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [8, 10]
            },
            {
                "nama": "Teknologi Blockchain",
                "nama_english": "Blockchain Technology",
                "kode": "CS127",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 7,
                "status": "aktif",
                "dosen_ids": [3, 9]
            },
            {
                "nama": "Data Mining",
                "nama_english": "Data Mining",
                "kode": "CS128",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [4, 6]
            },
            {
                "nama": "Analisis Data",
                "nama_english": "Data Analysis",
                "kode": "CS129",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [5, 11]
            },
            {
                "nama": "Game Development",
                "nama_english": "Game Development",
                "kode": "CS130",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 7,
                "status": "aktif",
                "dosen_ids": [7, 10]
            },
            {
                "nama": "Pemrograman C++",
                "nama_english": "C++ Programming",
                "kode": "CS131",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [3, 4]
            },
            {
                "nama": "Metode Numerik",
                "nama_english": "Numerical Methods",
                "kode": "MATH105",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 5,
                "status": "aktif",
                "dosen_ids": [6, 9]
            },
            {
                "nama": "Algoritma Genetika",
                "nama_english": "Genetic Algorithms",
                "kode": "CS132",
                "tipe": "Pilihan",
                "sks": 4,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [4, 8]
            },
            {
                "nama": "Sistem Pendukung Keputusan",
                "nama_english": "Decision Support Systems",
                "kode": "CS133",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 6,
                "status": "aktif",
                "dosen_ids": [5, 11]
            },
            {
                "nama": "Teori Graf",
                "nama_english": "Graph Theory",
                "kode": "MATH106",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 3,
                "status": "aktif",
                "dosen_ids": [3, 7]
            },
            {
                "nama": "Pengantar Sistem Informasi",
                "nama_english": "Introduction to Information Systems",
                "kode": "CS134",
                "tipe": "Wajib",
                "sks": 3,
                "semester": 2,
                "status": "aktif",
                "dosen_ids": [4, 10]
            }
            ]


        for mata_kuliah in mata_kuliah_data:
            serializer = MataKuliahSerializer(data=mata_kuliah)
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS(f"Created mata kuliah: {mata_kuliah['nama']}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to create mata kuliah: {mata_kuliah['nama']} - {serializer.errors}"))
