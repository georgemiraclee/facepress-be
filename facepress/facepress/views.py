from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .auth.permissions import IsAdmin, IsDosen, IsMahasiswa
from rest_framework.permissions import IsAuthenticated


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome Admin!"})

class DosenOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsDosen]

    def get(self, request):
        return Response({"message": "Welcome Dosen!"})

class MahasiswaOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]

    def get(self, request):
        return Response({"message": "Welcome Mahasiswa!"})
