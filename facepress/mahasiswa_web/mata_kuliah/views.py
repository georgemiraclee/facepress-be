from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from .serializers import MataKuliahMahasiswaSerializer, KelasSerializer
from admin_web.models import Mahasiswa, MataKuliahMahasiswa, MataKuliah, Kelas, JadwalKelas, PresensiMahasiswa
from facepress.auth.permissions import IsMahasiswa 

class MataKuliahMahasiswaListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Memeriksa apakah user adalah mahasiswa
        if user.role == 'mahasiswa':
            try:
                mahasiswa = Mahasiswa.objects.get(user=user)
                mata_kuliah_mahasiswa = MataKuliahMahasiswa.objects.filter(mahasiswa=mahasiswa)
                serializer = MataKuliahMahasiswaSerializer(mata_kuliah_mahasiswa, many=True)
                return Response({
                    "status": "success",
                    "message": "List of courses retrieved successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Mahasiswa.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Mahasiswa not found",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "status": "error",
                "message": "User is not a mahasiswa",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
        

class KelasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsMahasiswa]
    serializer_class = KelasSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            mahasiswa = user.mahasiswa
            return Kelas.objects.filter(mata_kuliah__mahasiswas=mahasiswa)
        except Mahasiswa.DoesNotExist:
            return Kelas.objects.none()

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
        
        # Fetch presensi for the current mahasiswa
        user = request.user
        try:
            mahasiswa = user.mahasiswa
            presensi_records = PresensiMahasiswa.objects.filter(mahasiswa=mahasiswa, jadwal_kelas__kelas=instance)
            presensi_map = {record.jadwal_kelas.id: record for record in presensi_records}  # Create a mapping by jadwal ID
        except Mahasiswa.DoesNotExist:
            presensi_map = {}

        jadwal_data = [{
            'id': jadwal.id,
            'tanggal': jadwal.tanggal,
            'jam_mulai': jadwal.jam_mulai,
            'jam_selesai': jadwal.jam_selesai,
            'dosen': jadwal.dosen.nama if jadwal.dosen else None,
            'ruang': jadwal.ruang.nama_ruang if jadwal.ruang else None,
            'status': jadwal.status,
            'presensi': {
                'tanggal_presensi': presensi_map[jadwal.id].tanggal_presensi if jadwal.id in presensi_map else None,
                'status': presensi_map[jadwal.id].status if jadwal.id in presensi_map else None,
                'presensi_oleh': presensi_map[jadwal.id].presensi_oleh if jadwal.id in presensi_map else None,
            }
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
            'jadwals': jadwal_data  # Include jadwal data with presensi
        }

        return Response({
            "success": True,
            "data": kelas_data,
            "message": "Kelas retrieved successfully."
        }, status=status.HTTP_200_OK)