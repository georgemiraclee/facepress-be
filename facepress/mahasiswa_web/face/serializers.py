from rest_framework import serializers
from admin_web.models import FaceDataset, WajahMahasiswa

class FaceDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceDataset
        fields = ['image_1', 'image_2', 'image_3']

    def create(self, validated_data):
        # Proses validasi atau pre-processing foto wajah dapat dilakukan di sini
        return super().create(validated_data)
    

class WajahMahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WajahMahasiswa
        fields = ['mahasiswa', 'image', 'created_at']
