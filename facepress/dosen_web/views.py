
from django.shortcuts import render
from rest_framework.views import APIView

class WebcamTestView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'dosen_web/test_webcam.html')
