from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from admin_web.models import User, Admin, Dosen, Mahasiswa

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('admin', 'Admin'), ('dosen', 'Dosen'), ('mahasiswa', 'Mahasiswa')])

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        # Validasi pengguna berdasarkan role
        user = None
        if role == 'admin':
            try:
                user = User.objects.get(email=email, role='admin')
                admin_profile = Admin.objects.get(email=email)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Admin tidak ditemukan")
        elif role == 'dosen':
            try:
                user = User.objects.get(email=email, role='dosen')
                dosen_profile = Dosen.objects.get(email=email)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Dosen tidak ditemukan")
        elif role == 'mahasiswa':
            try:
                user = User.objects.get(email=email, role='mahasiswa')
                mahasiswa_profile = Mahasiswa.objects.get(email=email)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Mahasiswa tidak ditemukan")
        
        # Cek password
        if user and not user.check_password(password):
            raise serializers.ValidationError("Password salah")
        
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': role,
        }
