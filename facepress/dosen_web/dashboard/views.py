from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DosenSerializer, JadwalKelasSerializer
from django.utils import timezone
from admin_web.models import JadwalKelas


class ProfilDosenView(generics.RetrieveAPIView):
    serializer_class = DosenSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.dosen

    def get(self, request, *args, **kwargs):
        dosen = self.get_object()
        serializer = self.get_serializer(dosen)
        response_data = {
            "status": "success",
            "message": "Data retrieved successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=200)


class JadwalTerdekatView(generics.ListAPIView):
    serializer_class = JadwalKelasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dosen = self.request.user.dosen
        today = timezone.now().date()
        return JadwalKelas.objects.filter(dosen=dosen, tanggal__gte=today).order_by('tanggal', 'jam_mulai')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
    
        response_data = {
            "status": "success",
            "message": "Nearest schedule retrieved successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=200)

