from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MahasiswaSerializer
from admin_web.models import Mahasiswa
from django.contrib.auth.hashers import make_password

class ProfilMahasiswaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Memeriksa apakah user adalah mahasiswa
        if user.role == 'mahasiswa':
            try:
                mahasiswa = Mahasiswa.objects.get(user=user)
                serializer = MahasiswaSerializer(mahasiswa)
                return Response({
                    "status": "success",
                    "message": "Profile retrieved successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Mahasiswa.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Mahasiswa not found",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "status": "error",
                "message": "User is not a mahasiswa",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)

class MahasiswaProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        # Get the Mahasiswa instance for the authenticated user
        return Mahasiswa.objects.get(user=user)

    def put(self, request):
        mahasiswa = self.get_object(request.user)
        
        # Create a dictionary to store the data for serialization
        update_data = request.data.copy()

        # If password is provided, hash it and set it on the mahasiswa instance
        password = update_data.get('password', None)
        if password:
            mahasiswa.user.password = make_password(password)  # Hash the password for the user
            mahasiswa.user.save()  # Save the user with the new password

        # Exclude the email from being updated
        if 'email' in update_data:
            del update_data['email']

        serializer = MahasiswaSerializer(mahasiswa, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": serializer.data,
                "message": "Profile updated successfully."
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "errors": serializer.errors,
            "message": "Profile update failed."
        }, status=status.HTTP_400_BAD_REQUEST)
