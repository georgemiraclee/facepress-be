from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Ruang, Kelas, JadwalKelas
from .serializers import RuangSerializer
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsAdmin 

class RuangViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]  
    queryset = Ruang.objects.all()
    serializer_class = RuangSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Ruang retrieved successfully."
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            ruang = self.get_object()
            serializer = self.get_serializer(ruang)
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Detail ruang retrieved successfully."
            }, status=status.HTTP_200_OK)
        except Ruang.DoesNotExist:
            return Response({
                "success": False,
                "error": "Ruang not found."
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            ruang_id = kwargs.get('pk')
            try:
                ruang = Ruang.objects.get(id=ruang_id)
            except Ruang.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Ruang not found."
                }, status=status.HTTP_404_NOT_FOUND)

            kelas_count = Kelas.objects.filter(ruang_id=ruang_id).count()
            jadwal_count = JadwalKelas.objects.filter(ruang_id=ruang_id).count()

            if kelas_count > 0 or jadwal_count > 0:
                return Response({
                    "success": False,
                    "message": "Ruang terdaftar di beberapa Kelas dan Jadwal Kelas. Ganti terlebih dahulu jika ingin menghapus."
                }, status=status.HTTP_400_BAD_REQUEST)

            ruang.delete()

            return Response({
                "success": True,
                "message": "Ruang deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    