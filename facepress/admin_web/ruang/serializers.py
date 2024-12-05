from rest_framework import serializers
from ..models import Ruang


class RuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruang
        fields = ['id', 'nama_ruang','lokasi']