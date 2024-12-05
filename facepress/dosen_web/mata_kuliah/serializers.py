from rest_framework import serializers
from admin_web.models import Dosen,  MataKuliah

class DosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = ['email', 'nip', 'nama', 'mobile_phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

class MataKuliahSerializer(serializers.ModelSerializer):
    dosens = DosenSerializer(many=True, read_only=True)
    dosen_ids = serializers.ListField(write_only=True, child=serializers.IntegerField(), required=False)

    class Meta:
        model = MataKuliah
        fields = ['id', 'nama', 'nama_english', 'kode', 'tipe', 'sks', 'semester', 'status', 'dosens', 'dosen_ids']
