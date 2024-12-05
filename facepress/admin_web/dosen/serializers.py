from rest_framework import serializers
from ..models import Dosen

# Dosen
class DosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = ['id','email', 'nip', 'nama', 'mobile_phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        dosen = super().create(validated_data)
        if password:
            dosen.set_password(password)
        dosen.save()
        return dosen


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        dosen = super().update(instance, validated_data)
        if password:
            dosen.set_password(password)
        dosen.save()
        return dosen