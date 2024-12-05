from rest_framework import viewsets, status
from rest_framework.response import Response
from admin_web.models import MataKuliah, Kelas, MataKuliahDosen
from .serializers import MataKuliahSerializer
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsDosen

class MataKuliahViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDosen]  
    serializer_class = MataKuliahSerializer

    def get_queryset(self):
        # Filter berdasarkan dosen yang sedang login
        if hasattr(self.request.user, 'dosen'):
            return MataKuliah.objects.filter(dosens=self.request.user.dosen)
        return MataKuliah.objects.none()  # Jika bukan dosen, return kosong

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Mata Kuliah retrieved successfully."
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        mata_kuliah_serializer = self.get_serializer(instance)
        kelas_queryset = Kelas.objects.filter(mata_kuliah=instance)
        kelas_data = []
        for kelas in kelas_queryset:
            kelas_data.append({
                "id": kelas.id,
                "nama_kelas": kelas.nama_kelas,
                "kode_kelas": kelas.kode_kelas,
                "ruang": {
                    "nama_ruang": kelas.ruang.nama_ruang if kelas.ruang else None,
                    "lokasi": kelas.ruang.lokasi if kelas.ruang else None
                },
                "hari": kelas.hari,
                "jam_mulai": kelas.jam_mulai,
                "jam_selesai": kelas.jam_selesai,
                "kapasitas": kelas.kapasitas,
            })

        return Response({
            "success": True,
            "data": {
                "mata_kuliah": mata_kuliah_serializer.data,
                "kelas": kelas_data
            },
            "message": "Kelas retrieved successfully."
        }, status=status.HTTP_200_OK)
