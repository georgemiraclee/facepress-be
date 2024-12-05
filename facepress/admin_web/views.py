from django.shortcuts import render
from rest_framework.views import APIView
from .models import Mahasiswa, Dosen, Ruang, MataKuliah, Kelas, JadwalKelas, MataKuliahDosen
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsAdmin 


class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, *args, **kwargs):
        try:
            total_mahasiswa = Mahasiswa.objects.count()
            total_dosen = Dosen.objects.count()
            total_mata_kuliah = MataKuliah.objects.count()
            total_kelas = Kelas.objects.count()

            response_data = {
                "totalMahasiswa": total_mahasiswa,
                "totalDosen": total_dosen,
                "totalMataKuliah": total_mata_kuliah,
                "totalKelas": total_kelas,
            }

            return Response({
                "success": True,
                "data": response_data,
                "message": "Dashboard data retrieved successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": str(e)
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
