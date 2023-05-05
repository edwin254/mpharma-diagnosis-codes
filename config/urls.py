"""diagnosis_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include('diagnosis_codes.urls')),
    path('api/diagnosis', include('diagnosis_codes.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/mpharma/docs/', include_docs_urls(title='Mpharm Diagnosis Api')) ,

]
