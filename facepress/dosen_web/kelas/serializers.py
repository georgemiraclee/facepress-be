from rest_framework import serializers
from admin_web.models import Ruang, Kelas

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

    def create(self, validated_data):
        mata_kuliah_id = self.context['mata_kuliah_id']
        ruang_id = validated_data.pop('ruang_id')
        
        kelas = Kelas.objects.create(**validated_data, mata_kuliah_id=mata_kuliah_id, ruang_id=ruang_id)
        return kelas
    def update(self, instance, validated_data):
        instance.nama_kelas = validated_data.get('nama_kelas', instance.nama_kelas)
        instance.kode_kelas = validated_data.get('kode_kelas', instance.kode_kelas)
        instance.ruang_id = validated_data.get('ruang_id', instance.ruang_id)
        instance.hari = validated_data.get('hari', instance.hari)
        instance.jam_mulai = validated_data.get('jam_mulai', instance.jam_mulai)
        instance.jam_selesai = validated_data.get('jam_selesai', instance.jam_selesai)
        instance.kapasitas = validated_data.get('kapasitas', instance.kapasitas)
    

        instance.save()
        return instance