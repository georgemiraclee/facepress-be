from rest_framework import viewsets, status
from ..models import Mahasiswa, Dosen, Ruang, MataKuliah, Kelas, JadwalKelas, MataKuliahDosen, User
from .serializers import DosenSerializer
from rest_framework.response import Response
from facepress.auth.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

class DosenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Dosen.objects.all()
    serializer_class = DosenSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.create_user(email=email, password=password, role='dosen')
        
        dosen = Dosen.objects.create(user=user, **request.data)
        
        serializer = self.get_serializer(dosen)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Dosen created successfully."
        }, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Dosen retrieved successfully."
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            dosen = self.get_object()
            serializer = self.get_serializer(dosen)
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Detail dosen retrieved successfully."
            }, status=status.HTTP_200_OK)
        except Dosen.DoesNotExist:
            return Response({
                "success": False,
                "error": "Dosen not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            # Ambil instance dosen berdasarkan pk
            dosen = self.get_object()
            # Simpan user yang terkait dengan dosen
            user = dosen.user

            # Cek apakah dosen terdaftar di Mata Kuliah
            mata_kuliah_count = MataKuliahDosen.objects.filter(dosen_id=dosen.id).count()
            
            # Cek apakah dosen terdaftar di Jadwal Kelas
            jadwal_count = JadwalKelas.objects.filter(dosen_id=dosen.id).count()

            # Jika terdaftar di Mata Kuliah atau Jadwal Kelas, tidak bisa dihapus
            if mata_kuliah_count > 0 or jadwal_count > 0:
                return Response({
                    "success": False,
                    "message": "Dosen terdaftar di beberapa Mata Kuliah dan Jadwal Kelas. Ganti terlebih dahulu jika ingin menghapus."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Hapus dosen terlebih dahulu
            dosen.delete()
            # Hapus user terkait
            user.delete()

            return Response({
                "success": True,
                "message": "Dosen and user deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)

        except Dosen.DoesNotExist:
            return Response({
                "success": False,
                "error": "Dosen not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
