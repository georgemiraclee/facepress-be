from rest_framework import serializers
from admin_web.models import Dosen

class DosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = ['id', 'nama', 'nip', 'email', 'mobile_phone']  # Removed the source for mobile_phone
from rest_framework import serializers
from admin_web.models import JadwalKelas, MataKuliah

class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = ['id', 'nama', 'nama_english', 'kode', 'tipe', 'sks', 'semester', 'status']

class JadwalKelasSerializer(serializers.ModelSerializer):
    matakuliah = MataKuliahSerializer(source='mata_kuliah')

    class Meta:
        model = JadwalKelas
        fields = ['id', 'tanggal', 'jam_mulai', 'jam_selesai', 'mata_kuliah', 'kelas', 'ruang', 'dosen', 'status', 'matakuliah']

