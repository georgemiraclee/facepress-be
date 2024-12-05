from rest_framework import serializers
from ..models import Mahasiswa, PresensiMahasiswa
from django.contrib.auth.hashers import make_password

class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = ['id', 'email', 'nim', 'nama', 'semester', 'is_wajah_exist', 'mobile_phone', 'nik', 'password']


    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        mahasiswa = Mahasiswa(**validated_data)
        mahasiswa.password = hashed_password
        
        mahasiswa.save()
        return mahasiswa

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
from ..models import MataKuliahMahasiswa, Mahasiswa, MataKuliah, Kelas


class MataKuliahMahasiswaSerializer(serializers.ModelSerializer):
    mata_kuliah_nama = serializers.CharField(source='mata_kuliah.nama', read_only=True)
    mata_kuliah_kode = serializers.CharField(source='mata_kuliah.kode', read_only=True)
    kelas_nama = serializers.CharField(source='kelas.nama_kelas', read_only=True)
    kelas_kode = serializers.CharField(source='kelas.kode', read_only=True)
    ruang_nama = serializers.CharField(source='kelas.ruang.nama', read_only=True)
    dosen_nama = serializers.CharField(source='kelas.mata_kuliah.dosen.nama', read_only=True)

    class Meta:
        model = MataKuliahMahasiswa
        fields = ['id', 'mahasiswa', 'mata_kuliah', 'kelas', 'semester_mengambil', 'status',
                  'mata_kuliah_nama', 'mata_kuliah_kode', 'kelas_nama', 'kelas_kode', 'ruang_nama', 'dosen_nama']
        extra_kwargs = {
            'mahasiswa': {'read_only': True},
            'semester_mengambil': {'read_only': True},
            'status': {'read_only': True}
        }

    def validate(self, attrs):
        if 'mata_kuliah' not in attrs or attrs['mata_kuliah'] is None:
            raise serializers.ValidationError({'mata_kuliah': 'This field cannot be null.'})
        if 'kelas' not in attrs or attrs['kelas'] is None:
            raise serializers.ValidationError({'kelas': 'This field cannot be null.'})
        return attrs
    

class PresensiMahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresensiMahasiswa
        fields = ['id', 'mahasiswa', 'mata_kuliah', 'kelas', 'jadwal_kelas', 'status', 'presensi_oleh', 'tanggal_presensi']

