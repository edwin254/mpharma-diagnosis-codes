from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient


class UploadFileViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.login(username='your_username', password='your_password')
        self.url = reverse('upload_file')

    def test_file_upload_success(self):
        # Create a dummy Tets CSV file
        csv_data = "category,code,full_code,abbreviated_description,full_description\n" \
                   "cat1,100,A001,desc1,full_desc1\n" \
                   "cat2,101,A002,desc2,full_desc2\n"
        file_data = BytesIO(csv_data.encode())
        file_data.name = 'test.csv'

        # Make a POST request to the view
        response = self.client.post(self.url, {'file': file_data, 'version': 'ICD-10'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'status': 'success'})

    def test_file_upload_bad_request(self):
        # Create a dummy image file
        image_file = BytesIO()
        Image.new('RGB', (100, 100)).save(image_file, 'jpeg')
        image_file.name = 'test.jpg'

        # Make a POST request with an image file (which should fail)
        response = self.client.post(self.url, {'file': image_file, 'version': 'ICD-10'})

        # Check that the response is a bad request and contains the expected error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'file': ['Invalid file. Check the encoding type..']})
