from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .mahasiswa.views import MahasiswaViewSet, MataKuliahMahasiswaViewSet,detail_jadwal_dan_mahasiswa, set_presensi_status
from .dosen.views import DosenViewSet
from .ruang.views import RuangViewSet
from .mata_kuliah.views import MataKuliahViewSet,JadwalKelasViewSet, CreateUpdateJadwalKelasView, KelasViewSet
from .views import DashboardDataView

router = DefaultRouter()

router.register(r'mahasiswa', MahasiswaViewSet, basename='admin-mahasiswa')
router.register(r'dosen', DosenViewSet, basename='admin-dosen')
router.register(r'ruang', RuangViewSet, basename='admin-ruang')
router.register(r'mata-kuliah', MataKuliahViewSet, basename='admin-mata_kuliah')
router.register(r'mahasiswa/(?P<id>\d+)/mata-kuliah', MataKuliahMahasiswaViewSet, basename='mata-kuliah-mahasiswa')
router.register(r'kelas', KelasViewSet, basename='kelas')


router.register(r'jadwal', JadwalKelasViewSet, basename='admin-jadwal_kelas')

urlpatterns = [
    path('dashboard/', DashboardDataView.as_view(), name='admin-dashboard'),
    path('mata-kuliah/<int:mata_kuliah_id>/kelas/', KelasViewSet.as_view({'post': 'create'}), name='kelas-create-list'),
    path('mata-kuliah/<int:mata_kuliah_id>/kelas/<int:pk>/', KelasViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='kelas-detail'),
    path('kelas/<int:kelas_id>/jadwal/', CreateUpdateJadwalKelasView.as_view(), name='jadwal-kelas-create'),
    path('presensi/<int:jadwal_id>/', detail_jadwal_dan_mahasiswa, name='detail_jadwal_dan_mahasiswa'),
    path('presensi/<int:presensi_id>/set-status/', set_presensi_status, name='set_presensi_status'),
    path('', include(router.urls)),
]
