from rest_framework import viewsets, status
from rest_framework.response import Response
from admin_web.models import MataKuliah, Kelas, JadwalKelas
from .serializers import JadwalSerializer
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsDosen

class JadwalKelasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDosen]  
    queryset = JadwalKelas.objects.all()
    serializer_class = JadwalSerializer

    http_method_names = ['get', 'put', 'patch', 'delete']


    def update(self, request, *args, **kwargs):
        try:
            jadwal = self.get_object()
            data = request.data

            kelas_id = data.get('kelas', jadwal.kelas.id)
            dosen_id = data.get('dosen', jadwal.dosen.id)

            # Validasi Kelas
            try:
                kelas = Kelas.objects.get(id=kelas_id)
            except Kelas.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Kelas not found."
                }, status=status.HTTP_404_NOT_FOUND)

            mata_kuliah_id = kelas.mata_kuliah.id
            ruang_id = kelas.ruang.id

            mata_kuliah = MataKuliah.objects.prefetch_related('dosens').get(id=mata_kuliah_id)
            dosen_ids = mata_kuliah.dosens.values_list('id', flat=True)
            if dosen_id not in dosen_ids:
                return Response({
                    "success": False,
                    "error": "Dosen is not assigned to this Mata Kuliah."
                }, status=status.HTTP_400_BAD_REQUEST)

            valid_status = ['belum dimulai', 'sedang berlangsung', 'sudah selesai']
            status_jadwal = data.get('status', jadwal.status)
            if status_jadwal not in valid_status:
                status_jadwal = 'belum dimulai'

            jadwal_data = {
                'kelas': kelas_id,
                'tanggal': data.get('tanggal', jadwal.tanggal),
                'jam_mulai': data.get('jam_mulai', jadwal.jam_mulai),
                'jam_selesai': data.get('jam_selesai', jadwal.jam_selesai),
                'dosen': dosen_id,
                'mata_kuliah': mata_kuliah_id,
                'ruang': ruang_id,
                'status': status_jadwal,
            }

            serializer = self.get_serializer(jadwal, data=jadwal_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Jadwal Kelas updated successfully."
            }, status=status.HTTP_200_OK)

        except MataKuliah.DoesNotExist:
            return Response({
                "success": False,
                "error": "Mata Kuliah not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_kelas(self, kelas_id):
        try:
            return Kelas.objects.get(id=kelas_id)
        except Kelas.DoesNotExist:
            return None

    def validate_dosen(self, mata_kuliah_id, dosen_id):
        try:
            mata_kuliah = MataKuliah.objects.prefetch_related('dosens').get(id=mata_kuliah_id)
            dosen_ids = mata_kuliah.dosens.values_list('id', flat=True)
            return dosen_id in dosen_ids
        except MataKuliah.DoesNotExist:
            return False

    def prepare_jadwal_data(self, request_data, kelas_id, dosen_id, mata_kuliah_id, ruang_id):
        valid_status = ['belum dimulai', 'sedang berlangsung', 'sudah selesai']
        status_jadwal = request_data.get('status', 'belum dimulai')
        if status_jadwal not in valid_status:
            status_jadwal = 'belum dimulai'

        return {
            'kelas': kelas_id,
            'tanggal': request_data.get('tanggal'),
            'jam_mulai': request_data.get('jam_mulai'),
            'jam_selesai': request_data.get('jam_selesai'),
            'dosen': dosen_id,
            'mata_kuliah': mata_kuliah_id,
            'ruang': ruang_id,
            'status': status_jadwal,
        }