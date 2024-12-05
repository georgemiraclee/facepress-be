from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from admin_web.models import FaceDataset, Mahasiswa, WajahMahasiswa
from .serializers import FaceDatasetSerializer
from mtcnn import MTCNN
from PIL import Image
import numpy as np
from rest_framework.permissions import IsAuthenticated
from facepress.auth.permissions import IsMahasiswa 
import cv2
from .serializers import WajahMahasiswaSerializer
import os
from django.conf import settings
from facepress.auth.permissions import IsMahasiswa 

class FaceDatasetView(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]

    def post(self, request, *args, **kwargs):
        # Ambil mahasiswa yang sedang login berdasarkan request.user
        try:
            mahasiswa = Mahasiswa.objects.get(user=request.user)  # Dapatkan instance Mahasiswa
        except Mahasiswa.DoesNotExist:
            return Response({'error': 'Mahasiswa tidak ditemukan.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FaceDatasetSerializer(data=request.data)
        
        if serializer.is_valid():
            # Ambil foto yang di-upload
            image_1 = request.FILES['image_1']
            image_2 = request.FILES['image_2']
            image_3 = request.FILES['image_3']
            
            # Convert images to arrays and ensure they are in RGB format
            img1 = Image.open(image_1).convert('RGB')
            img2 = Image.open(image_2).convert('RGB')
            img3 = Image.open(image_3).convert('RGB')

            img1_array = np.array(img1)
            img2_array = np.array(img2)
            img3_array = np.array(img3)

            # Deteksi wajah dengan MTCNN
            detector = MTCNN()
            faces_img1_mtcnn = detector.detect_faces(img1_array)
            faces_img2_mtcnn = detector.detect_faces(img2_array)
            faces_img3_mtcnn = detector.detect_faces(img3_array)

            # Validasi bahwa wajah ditemukan di setiap gambar
            errors = []
            if len(faces_img1_mtcnn) == 0:
                errors.append('Wajah tidak terdeteksi pada gambar 1.')
            if len(faces_img2_mtcnn) == 0:
                errors.append('Wajah tidak terdeteksi pada gambar 2.')
            if len(faces_img3_mtcnn) == 0:
                errors.append('Wajah tidak terdeteksi pada gambar 3.')

            if errors:
                return Response({'error': errors}, status=status.HTTP_400_BAD_REQUEST)

            # Jika semua validasi lolos, simpan dataset
            face_dataset = FaceDataset(
                mahasiswa=mahasiswa,  # Assign instance Mahasiswa
                image_1=image_1,
                image_2=image_2,
                image_3=image_3
            )
            face_dataset.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaptureFaceDataset(APIView):
    permission_classes = [IsAuthenticated, IsMahasiswa]

    def post(self, request, *args, **kwargs):
        try:
            mahasiswa = request.user.mahasiswa
        except Mahasiswa.DoesNotExist:
            return Response({"detail": "Mahasiswa tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        # Cek jika sudah ada 10 foto untuk mahasiswa ini
        if WajahMahasiswa.objects.filter(mahasiswa=mahasiswa).count() >= 10:
            return Response({"detail": "Dataset wajah sudah lengkap."}, status=status.HTTP_400_BAD_REQUEST)

        # Directory to save images
        save_dir = os.path.join(settings.MEDIA_ROOT, 'wajah_mahasiswa')
        os.makedirs(save_dir, exist_ok=True)

        # Buka kamera
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        count = 0
        captured_images = []

        while count < 10:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) > 0:
                # Simpan gambar ke filesystem
                image_filename = f"{mahasiswa.nim}_{count}.jpg"
                image_filename_database = f"wajah_mahasiswa/{mahasiswa.nim}_{count}.jpg"
                image_path = os.path.join(save_dir, image_filename)
                cv2.imwrite(image_path, frame)

                # Simpan nama file ke database
                wajah_instance = WajahMahasiswa.objects.create(mahasiswa=mahasiswa, image=image_filename_database)
                serializer = WajahMahasiswaSerializer(wajah_instance)
                captured_images.append(serializer.data)
                
                count += 1

        # Tutup kamera
        cap.release()

        return Response({"captured_images": captured_images}, status=status.HTTP_201_CREATED)