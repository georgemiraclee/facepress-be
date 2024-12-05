from rest_framework import serializers
from admin_web.models import PresensiMahasiswa


class PresensiMahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresensiMahasiswa
        fields = ['id', 'mahasiswa', 'mata_kuliah', 'kelas', 'jadwal_kelas', 'status', 'presensi_oleh', 'tanggal_presensi']