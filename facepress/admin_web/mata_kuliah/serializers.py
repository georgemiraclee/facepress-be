from rest_framework import serializers
from ..models import Mahasiswa, Dosen, Ruang, MataKuliah, Kelas, JadwalKelas
from ..dosen.serializers import DosenSerializer
from ..ruang.serializers import RuangSerializer

class MataKuliahSerializer(serializers.ModelSerializer):
    dosens = DosenSerializer(many=True, read_only=True)
    dosen_ids = serializers.ListField(write_only=True, child=serializers.IntegerField(), required=False)

    class Meta:
        model = MataKuliah
        fields = ['id', 'nama', 'nama_english', 'kode', 'tipe', 'sks', 'semester', 'status', 'dosens', 'dosen_ids']

    def create(self, validated_data):
        dosen_ids = validated_data.pop('dosen_ids', [])
        mata_kuliah = MataKuliah.objects.create(**validated_data)
        
        # Assign dosens to MataKuliah
        if dosen_ids:
            dosens = Dosen.objects.filter(id__in=dosen_ids)
            mata_kuliah.dosens.add(*dosens)
        
        return mata_kuliah

    def update(self, instance, validated_data):
        dosen_ids = validated_data.pop('dosen_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if dosen_ids is not None:
            dosens = Dosen.objects.filter(id__in=dosen_ids)
            instance.dosens.set(dosens)

        return instance
    
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
    
class JadwalKelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = JadwalKelas
        fields = ['id', 'tanggal', 'jam_mulai', 'jam_selesai', 'dosen']

    def create(self, validated_data):
        kelas_id = self.context['kelas_id']  
        
        try:
            kelas = Kelas.objects.get(id=kelas_id)
        except Kelas.DoesNotExist:
            raise serializers.ValidationError("Kelas not found.")

        mata_kuliah = kelas.mata_kuliah
        ruang = kelas.ruang

        validated_data['mata_kuliah'] = mata_kuliah
        validated_data['ruang'] = ruang
        validated_data['kelas'] = kelas

        # Tetapkan default status jika tidak ada
        if 'status' not in validated_data or not validated_data['status']:
            validated_data['status'] = 'belum dimulai'
        
        return super().create(validated_data)
    
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
