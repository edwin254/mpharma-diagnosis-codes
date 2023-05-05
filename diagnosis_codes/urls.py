from django.urls import path
from rest_framework import routers

from .views import DiagnosisICDViewSet, UploadFileView

router = routers.DefaultRouter()

router.register('', DiagnosisICDViewSet, 'diagnosis')

urlpatterns = router.urls
urlpatterns += [
    path('upload_codes', UploadFileView.as_view(), name="instances"),
]