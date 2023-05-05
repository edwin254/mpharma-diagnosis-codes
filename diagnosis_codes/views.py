import csv
import io
import json

import pandas as pd
import redis
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from diagnosis_codes.models import Diagnosis, DiagnosisCategory
from diagnosis_codes.utils import create_diagnoses

from .serializers import (DiagnosisCategorySerializer, DiagnosisICDSerializer,
                          FileUploadSerializer)


# DiagnosisCategorySerializer Viewset
class DiagnosisCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisCategorySerializer

# DiagnosisICDSerializer Viewset
class DiagnosisICDViewSet(viewsets.ModelViewSet):
    queryset = DiagnosisCategory.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = DiagnosisICDSerializer
    lookup_field  =  'full_code'

class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        diagnosis_data = serializer.validated_data['file']
        version = serializer.validated_data['version']

        names  = ['category' , 'code' , 'full_code', 'abbreviated_description' , 'full_description', 'category_title']
        data  = pd.read_csv(diagnosis_data , header=None , names= names)
        create_diagnoses(data=data, version=version)

        # publisher notification

        r = redis.Redis(host='localhost', port=6379, db=0)
        r.publish('diagnosis_upload', json.dumps({"receiver": request.user.email, "record_count": data.shape[0]}))

        return Response({"status": "success"},
                        status.HTTP_201_CREATED)