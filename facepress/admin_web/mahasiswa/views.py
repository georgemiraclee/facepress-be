from rest_framework import viewsets, status
from ..models import Mahasiswa, Kelas, MataKuliahMahasiswa, JadwalKelas, PresensiMahasiswa, User
from .serializers import MahasiswaSerializer, MataKuliahMahasiswaSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .serializers import PresensiMahasiswaSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsAdmin 

class MahasiswaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Mahasiswa.objects.all() 
    serializer_class = MahasiswaSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.create_user(email=email, password=password, role='mahasiswa')
        
        mahasiswa = Mahasiswa.objects.create(user=user, **request.data)
        
        serializer = self.get_serializer(mahasiswa)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Mahasiswa created successfully."
        }, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Mahasiswa retrieved successfully."
        }, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            mahasiswa = self.get_object()
            serializer = self.get_serializer(mahasiswa)
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Detail mahasiswa retrieved successfully."
            }, status=status.HTTP_200_OK)
        except Mahasiswa.DoesNotExist:
            return Response({
                "success": False,
                "error": "Mahasiswa not found."
            }, status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        try:
            mahasiswa = self.get_object()
            user = mahasiswa.user
            mahasiswa.delete()
            user.delete()
            return Response({
                "success": True,
                "message": "Mahasiswa and user deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except Mahasiswa.DoesNotExist:
            return Response({
                "success": False,
                "error": "Mahasiswa not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
class MataKuliahMahasiswaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = MataKuliahMahasiswa.objects.all()
    serializer_class = MataKuliahMahasiswaSerializer

    def create(self, request, *args, **kwargs):
        mahasiswa_id = kwargs.get('id')
        mata_kuliah_id = request.data.get('mata_kuliah')
        kelas_id = request.data.get('kelas')

        try:
            with transaction.atomic():
                mahasiswa = Mahasiswa.objects.filter(id=mahasiswa_id).first()
                if not mahasiswa:
                    return Response({'error': 'Mahasiswa not found'}, status=status.HTTP_404_NOT_FOUND)
                print(kelas_id)
                print(mata_kuliah_id)

                kelas = Kelas.objects.filter(id=kelas_id, mata_kuliah_id=mata_kuliah_id).first()
                if not kelas:
                    return Response({'error': 'Kelas does not belong to the given MataKuliah'}, status=status.HTTP_400_BAD_REQUEST)

                existing_record = MataKuliahMahasiswa.objects.filter(mahasiswa_id=mahasiswa_id, mata_kuliah_id=mata_kuliah_id).first()
                if existing_record:
                    return Response({'error': 'Mahasiswa has already taken this MataKuliah'}, status=status.HTTP_400_BAD_REQUEST)

                new_record = MataKuliahMahasiswa.objects.create(
                    mahasiswa_id=mahasiswa_id,
                    mata_kuliah_id=mata_kuliah_id,
                    kelas_id=kelas_id,
                    semester_mengambil=mahasiswa.semester,
                    status="Belum Lulus"
                )

                jadwals = JadwalKelas.objects.filter(kelas_id=kelas_id)

                for jadwal in jadwals:
                    PresensiMahasiswa.objects.create(
                        mahasiswa_id=mahasiswa_id,
                        mata_kuliah_id=mata_kuliah_id,
                        kelas_id=kelas_id,
                        jadwal_kelas_id=jadwal.id,
                        status=None,
                        presensi_oleh=None,
                        tanggal_presensi=None
                    )

            return Response({'id': new_record.id, 'message': 'Record created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request, *args, **kwargs):
        mahasiswa_id = kwargs.get('id')
        try:
            records = MataKuliahMahasiswa.objects.filter(mahasiswa_id=mahasiswa_id).select_related(
                'mata_kuliah',
                'kelas'
            ).prefetch_related(
                'kelas__ruang',
                'kelas__mata_kuliah__dosens'
            )
            
            if not records.exists():
                return Response({'message': 'Records not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(records, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, *args, **kwargs):
        record_id = kwargs.get('pk')
        try:
            record = MataKuliahMahasiswa.objects.filter(id=record_id).first()
            if not record:
                return Response({'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

            record.delete()
            return Response({'message': 'Record deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        record_id = kwargs.get('pk')    
        try:
            record = MataKuliahMahasiswa.objects.filter(id=record_id).first()
            if not record:
                return Response({'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)

            mata_kuliah_id = request.data.get('mata_kuliah')
            kelas_id = request.data.get('kelas')

            record.mata_kuliah_id = mata_kuliah_id
            record.kelas_id = kelas_id
            record.semester_mengambil = record.mahasiswa.semester
            record.status = request.data.get('status', record.status)

            record.save()

            return Response({'message': 'Record updated successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin]) 
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

        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin]) 
def set_presensi_status(request, presensi_id):
    try:
        presensi = get_object_or_404(PresensiMahasiswa, id=presensi_id)

        status_baru = request.data.get('status')

        if status_baru not in dict(PresensiMahasiswa.STATUS_CHOICES).keys():
            raise ValidationError({'error': 'Status tidak valid'})

        presensi.status = status_baru
        presensi.presensi_oleh = 'admin'
        presensi.tanggal_presensi = timezone.now().date()
        presensi.save()

        serializer = PresensiMahasiswaSerializer(presensi)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValidationError as ve:
        return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)