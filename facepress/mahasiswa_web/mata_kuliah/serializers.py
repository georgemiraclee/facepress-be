from rest_framework import serializers
from admin_web.models import MataKuliahMahasiswa
from rest_framework import serializers
from admin_web.models import MataKuliahMahasiswa, Ruang, Kelas

class MataKuliahMahasiswaSerializer(serializers.ModelSerializer):
    mata_kuliah_nama = serializers.CharField(source='mata_kuliah.nama')
    kelas_nama = serializers.CharField(source='kelas.nama_kelas')

    class Meta:
        model = MataKuliahMahasiswa
        fields = ['mata_kuliah_nama', 'kelas_nama', 'semester_mengambil', 'status']

class RuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruang
        fields = ['nama_ruang','lokasi']

class KelasSerializer(serializers.ModelSerializer):
    ruang = RuangSerializer(read_only=True)
    ruang_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Kelas
        fields = ['id', 'nama_kelas', 'kode_kelas', 'ruang', 'ruang_id', 'hari', 'jam_mulai', 'jam_selesai', 'kapasitas']
