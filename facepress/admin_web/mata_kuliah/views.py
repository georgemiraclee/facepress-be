from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import MataKuliah, Kelas, JadwalKelas
from .serializers import  MataKuliahSerializer, KelasSerializer, JadwalKelasSerializer, JadwalSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsAdmin 

class MataKuliahViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]  
    queryset = MataKuliah.objects.all()
    serializer_class = MataKuliahSerializer

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        mata_kuliah = serializer.save()
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Mata Kuliah updated successfully."
        }, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, partial=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "success": True,
            "message": "Mata Kuliah berhasil dihapus."
        }, status=status.HTTP_200_OK)

class KelasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]  
    serializer_class = KelasSerializer

    def get_queryset(self):
        mata_kuliah_id = self.kwargs.get('mata_kuliah_id')
        if mata_kuliah_id:
            return Kelas.objects.filter(mata_kuliah__id=mata_kuliah_id)
        return Kelas.objects.all()

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

    def create(self, request, mata_kuliah_id=None):
        try:
            serializer = KelasSerializer(data=request.data, context={'mata_kuliah_id': mata_kuliah_id})
            serializer.is_valid(raise_exception=True)
            kelas = serializer.save()
            return Response({
                "success": True,
                "data": KelasSerializer(kelas).data,
                "message": "Kelas created successfully."
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success": False,
                "error": {
                    "code": "BAD_REQUEST",
                    "message": str(e)
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        jadwals = JadwalKelas.objects.filter(kelas=instance).select_related('dosen', 'ruang')
        jadwal_data = [{
            'id': jadwal.id,
            'tanggal': jadwal.tanggal,
            'jam_mulai': jadwal.jam_mulai,
            'jam_selesai': jadwal.jam_selesai,
            'dosen': jadwal.dosen.nama if jadwal.dosen else None,
            'ruang': jadwal.ruang.nama_ruang if jadwal.ruang else None,
            'status': jadwal.status
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
            'jadwals': jadwal_data
        }

        return Response({
            "success": True,
            "data": kelas_data,
            "message": "Kelas retrieved successfully."
        }, status=status.HTTP_200_OK)
    def update(self, request, pk=None, mata_kuliah_id=None, partial=False):
        try:
            kelas = self.get_object()
            serializer = KelasSerializer(kelas, data=request.data, partial=partial, context={'mata_kuliah_id': mata_kuliah_id}) 
            serializer.is_valid(raise_exception=True)
            updated_kelas = serializer.save()
            return Response({
                "success": True,
                "data": KelasSerializer(updated_kelas).data,
                "message": "Kelas updated successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "error": {
                    "code": "BAD_REQUEST",
                    "message": str(e)
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Delete Kelas
        return super().destroy(request, *args, **kwargs)
    
class JadwalKelasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]  
    queryset = JadwalKelas.objects.all()
    serializer_class = JadwalSerializer

    http_method_names = ['get', 'put', 'patch', 'delete']


    def create(self, request, *args, **kwargs):
        try:
            kelas_id = self.kwargs.get('kelas_id')
            dosen_id = request.data.get('dosen')

            # Validasi Kelas
            kelas = self.get_kelas(kelas_id)
            if kelas is None:
                return Response({
                    "success": False,
                    "error": "Kelas not found."
                }, status=status.HTTP_404_NOT_FOUND)

            mata_kuliah_id = kelas.mata_kuliah.id
            ruang_id = kelas.ruang.id

            if not self.validate_dosen(mata_kuliah_id, dosen_id):
                return Response({
                    "success": False,
                    "error": "Dosen is not assigned to this Mata Kuliah."
                }, status=status.HTTP_400_BAD_REQUEST)

            jadwal_data = self.prepare_jadwal_data(request.data, kelas_id, dosen_id, mata_kuliah_id, ruang_id)

            serializer = self.get_serializer(data=jadwal_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Jadwal Kelas created successfully."
            }, status=status.HTTP_201_CREATED)

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


    def destroy(self, request, *args, **kwargs):
        try:
            jadwal = self.get_object()
            jadwal.delete()
            return Response({
                "success": True,
                "message": "Jadwal Kelas deleted successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        except JadwalKelas.DoesNotExist:
            return Response({
                "success": False,
                "error": "Jadwal Kelas not found."
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

        
class CreateUpdateJadwalKelasView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]  
    serializer_class = JadwalKelasSerializer

    def post(self, request, kelas_id, *args, **kwargs):
        kelas = get_object_or_404(Kelas, id=kelas_id)
        mata_kuliah = kelas.mata_kuliah
        data = request.data
        data['mata_kuliah'] = mata_kuliah.id
        data['kelas'] = kelas.id

        serializer = self.get_serializer(data=data, context={'kelas_id': kelas_id})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Jadwal Kelas berhasil dibuat."
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, kelas_id, *args, **kwargs):
        kelas = get_object_or_404(Kelas, id=kelas_id)
        mata_kuliah = kelas.mata_kuliah
        jadwal_kelas = get_object_or_404(JadwalKelas, mata_kuliah=mata_kuliah, kelas=kelas)
        
        serializer = self.get_serializer(jadwal_kelas, data=request.data, partial=True, context={'kelas_id': kelas_id})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Jadwal Kelas berhasil diperbarui."
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class JadwalbyIDKelasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]  
    serializer_class = JadwalKelasSerializer

    def create(self, request, kelas_id):
        try:
            data = request.data
            kelas = get_object_or_404(Kelas, id=kelas_id)

            mata_kuliah_id = kelas.mata_kuliah.id
            ruang_id = kelas.ruang.id

            dosen_id = data.get('dosen')
            mata_kuliah = MataKuliah.objects.prefetch_related('dosens').get(id=mata_kuliah_id)
            dosen_ids = mata_kuliah.dosens.values_list('id', flat=True)

            if dosen_id not in dosen_ids:
                return Response({
                    "success": False,
                    "error": "Dosen is not assigned to this Mata Kuliah."
                }, status=status.HTTP_400_BAD_REQUEST)

            jadwal_data = {
                'kelas': kelas_id,
                'tanggal': data.get('tanggal'),
                'jam_mulai': data.get('jam_mulai'),
                'jam_selesai': data.get('jam_selesai'),
                'dosen': dosen_id,
                'mata_kuliah': mata_kuliah_id,
                'ruang': ruang_id,
                'status': data.get('status', 'belum dimulai'),
            }

            serializer = self.get_serializer(data=jadwal_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Jadwal Kelas created successfully."
            }, status=status.HTTP_201_CREATED)

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

    def update(self, request, kelas_id, *args, **kwargs):
        jadwal = self.get_object()
        serializer = self.get_serializer(jadwal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "data": serializer.data,
            "message": "Jadwal Kelas updated successfully."
        }, status=status.HTTP_200_OK)

    def destroy(self, request, kelas_id, *args, **kwargs):
        jadwal = self.get_object()
        jadwal.delete()
        return Response({
            "success": True,
            "message": "Jadwal Kelas berhasil dihapus."
        }, status=status.HTTP_204_NO_CONTENT)