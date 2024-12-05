from rest_framework import serializers
from admin_web.models import Kelas, JadwalKelas

class JadwalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JadwalKelas
        fields = ['id', 'tanggal', 'jam_mulai', 'jam_selesai', 'dosen', 'status']

    def create(self, validated_data):
        kelas_id = self.context['kelas_id']  

        kelas = self.get_kelas(kelas_id)
        if kelas is None:
            raise serializers.ValidationError("Kelas not found.")

        validated_data['mata_kuliah'] = kelas.mata_kuliah
        validated_data['ruang'] = kelas.ruang
        validated_data['kelas'] = kelas
        
        return super().create(validated_data)

    def get_kelas(self, kelas_id):
        try:
            return Kelas.objects.get(id=kelas_id)
        except Kelas.DoesNotExist:
            return None
