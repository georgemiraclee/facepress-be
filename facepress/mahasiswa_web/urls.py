from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .profile.views import ProfilMahasiswaAPIView, MahasiswaProfileUpdateView
from .mata_kuliah.views import MataKuliahMahasiswaListAPIView, KelasViewSet
from .face.views import FaceDatasetView, CaptureFaceDataset
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'kelas', KelasViewSet, basename='kelas')  # Fix here

urlpatterns = [
    path('profil-user/', ProfilMahasiswaAPIView.as_view(), name='profil-mahasiswa'),
    path('mata-kuliah/', MataKuliahMahasiswaListAPIView.as_view(), name='list-mata-kuliah'),
    path('profile/update/', MahasiswaProfileUpdateView.as_view(), name='mahasiswa-profile-update'),
    path('register-face/', FaceDatasetView.as_view(), name='register-face'),
    path('capture_wajah/', CaptureFaceDataset.as_view(), name='capture-wajah-mahasiswa'),


    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
