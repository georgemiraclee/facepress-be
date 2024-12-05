from rest_framework import  status
from admin_web.models import Mahasiswa,  JadwalKelas, PresensiMahasiswa
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .serializers import PresensiMahasiswaSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsDosen 

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDosen]) 
def detail_jadwal_dan_mahasiswa(request, jadwal_id):
    try:
        jadwal = get_object_or_404(JadwalKelas.objects.prefetch_related(
            'presensi',
            'mata_kuliah',
            'kelas',
            'ruang',
            'dosen',
        ), id=jadwal_id)

        presensi_mahasiswa_ids = [presensi.mahasiswa.id for presensi in jadwal.presensi.all()]

        mahasiswas = Mahasiswa.objects.filter(id__in=presensi_mahasiswa_ids).values(
            'id', 'nama', 'nim', 'email', 'semester', 'mobile_phone', 'nik'
        )

        result = {
            'id': jadwal.id,
            'tanggal': jadwal.tanggal,
            'jamMulai': jadwal.jam_mulai,
            'jamSelesai': jadwal.jam_selesai,
            'mataKuliah': jadwal.mata_kuliah.nama,
            'kelas': jadwal.kelas.nama_kelas,
            'ruang': jadwal.ruang.nama_ruang,
            'dosen': jadwal.dosen.nama,
            'presensiMahasiswa': [
                {
                     'presensiId': presensi.id,
                    'mahasiswaId': presensi.mahasiswa.id,
                    'namaMahasiswa': presensi.mahasiswa.nama,
                    'nimMahasiswa': presensi.mahasiswa.nim,
                    'emailMahasiswa': presensi.mahasiswa.email,
                    'statusPresensi': presensi.status,
                    'presensiOleh': presensi.presensi_oleh,
                    'tanggalPresensi': presensi.tanggal_presensi,
                } for presensi in jadwal.presensi.all()
            ],
        }

        return Response({
            "success": True,
            "data": result,
            "message": "Detail jadwal dan presensi mahasiswa retrieved successfully."
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "success": False,
            "message": "An error occurred while retrieving the data.",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsDosen]) 
def set_presensi_status(request, presensi_id):
    try:
        presensi = get_object_or_404(PresensiMahasiswa, id=presensi_id)

        status_baru = request.data.get('status')

        if status_baru not in dict(PresensiMahasiswa.STATUS_CHOICES).keys():
            raise ValidationError({'error': 'Status tidak valid'})

        presensi.status = status_baru
        presensi.presensi_oleh = 'dosen'
        presensi.tanggal_presensi = timezone.now().date()
        presensi.save()

        serializer = PresensiMahasiswaSerializer(presensi)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Status presensi updated successfully."
        }, status=status.HTTP_200_OK)

    except ValidationError as ve:
        return Response({
            "success": False,
            "message": "Validation error.",
            "errors": ve.detail
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "success": False,
            "message": "An error occurred while updating the presensi.",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
