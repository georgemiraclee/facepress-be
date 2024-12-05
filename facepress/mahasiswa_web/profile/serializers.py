from rest_framework import serializers
from admin_web.models import Mahasiswa

class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = ['nama', 'nim', 'email', 'semester', 'mobile_phone', 'nik','is_wajah_exist']
