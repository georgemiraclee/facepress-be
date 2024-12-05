from rest_framework import viewsets, status
from rest_framework.response import Response
from admin_web.models import MataKuliah, Kelas, JadwalKelas
from .serializers import   KelasSerializer
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsDosen

class KelasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDosen]  
    serializer_class = KelasSerializer

    def get_queryset(self):
        mata_kuliah_id = self.kwargs.get('mata_kuliah_id')
        if mata_kuliah_id:
            return Kelas.objects.filter(mata_kuliah__id=mata_kuliah_id)
        return Kelas.objects.all()

    def list(self, request, mata_kuliah_id=None):
        try:
            mata_kuliah = MataKuliah.objects.get(id=mata_kuliah_id)
            kelas = self.get_queryset()
            serializer = self.get_serializer(kelas, many=True)
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Kelas retrieved successfully."
            }, status=status.HTTP_200_OK)
        except MataKuliah.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "Mata Kuliah not found."
                }
            }, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        jadwals = JadwalKelas.objects.filter(kelas=instance).select_related('dosen', 'ruang')
        jadwal_data = [{
            'id': jadwal.id,
            'tanggal': jadwal.tanggal,
            'jam_mulai': jadwal.jam_mulai,
            'jam_selesai': jadwal.jam_selesai,
            'dosen': jadwal.dosen.nama if jadwal.dosen else None,
            'ruang': jadwal.ruang.nama_ruang if jadwal.ruang else None,
            'status': jadwal.status
        } for jadwal in jadwals]

        kelas_data = {
            'id': instance.id,
            'nama_kelas': instance.nama_kelas,
            'kode_kelas': instance.kode_kelas,
            'ruang': instance.ruang.nama_ruang if instance.ruang else None,
            'hari': instance.hari,
            'jam_mulai': instance.jam_mulai,
            'jam_selesai': instance.jam_selesai,
            'kapasitas': instance.kapasitas,
            'mata_kuliah': {
                'id': instance.mata_kuliah.id,
                'nama': instance.mata_kuliah.nama,
                'kode': instance.mata_kuliah.kode,
                'sks': instance.mata_kuliah.sks
            },
            'jadwals': jadwal_data
        }

        return Response({
            "success": True,
            "data": kelas_data,
            "message": "Kelas retrieved successfully."
        }, status=status.HTTP_200_OK)