from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Diagnosis, DiagnosisCategory, IcdVersion
from .serializers import (DiagnosisCategorySerializer, DiagnosisSerializer,
                          IcdVersionSerializer)


class DiagnosisTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.icd_version = IcdVersion.objects.create(version="ICD-10", description="International Classification of Diseases, 10th Revision")
        self.category = DiagnosisCategory.objects.create(code="A00", description="Cholera")
        self.diagnosis = Diagnosis.objects.create(category=self.category, icd_version=self.icd_version, code="A000", full_code="A0000", abbreviated_description="Cholera due to Vibrio cholerae 01, biovar cholerae", full_description="Cholera due to Vibrio cholerae 01, biovar cholerae")
        self.valid_payload = {
            'category': self.category.id,
            'icd_version': self.icd_version.id,
            'code': 'A001',
            'full_code': 'A0010',
            'abbreviated_description': 'Cholera due to Vibrio cholerae 01, biovar eltor',
            'full_description': 'Cholera due to Vibrio cholerae 01, biovar eltor'
        }
        self.invalid_payload = {
            'category': self.category.id,
            'icd_version': self.icd_version.id,
            'code': 'A002',
            'full_code': 'A0000',  # Duplicate full_code, this should cause a validation error
            'abbreviated_description': 'Cholera due to Vibrio cholerae 01, biovar ogawa',
            'full_description': 'Cholera due to Vibrio cholerae 01, biovar ogawa'
        }

    def test_get_all_diagnoses(self):
        url = reverse('diagnosis-list')
        response = self.client.get(url)
        diagnoses = Diagnosis.objects.all()
        serializer = DiagnosisSerializer(diagnoses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_valid_diagnosis(self):
        url = reverse('diagnosis-list')
        response = self.client.post(url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_diagnosis(self):
        url = reverse('diagnosis-list')
        response = self.client.post(url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_diagnosis(self):
        url = reverse('diagnosis-detail', kwargs={'full_code': self.diagnosis.full_code})
        response = self.client.get(url)
        serializer = DiagnosisSerializer(self.diagnosis)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_diagnosis(self):
        url = reverse('diagnosis-detail', kwargs={'full_code': self.diagnosis.full_code})
        new_data = {
            'abbreviated_description': 'New description'
        }
        response = self.client.patch(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['abbreviated_description'], new_data['abbreviated_description'])

    def test_delete_diagnosis(self):
        url = reverse('diagnosis-detail', kwargs={'full_code': self.diagnosis.full_code})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Diagnosis.objects.count(), 0)
