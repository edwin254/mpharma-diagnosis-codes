from rest_framework import serializers

from diagnosis_codes.models import Diagnosis, DiagnosisCategory


class EagerLoadingMixin:
  @classmethod
  def set_up_eager_loading(cls, queryset):
    print("Setting up eager loading...")
    if hasattr(cls, "_SELECT_RELATED_FIELDS"):
      queryset = queryset.select_related(*cls._SELECT_RELATED_FIELDS)
    if hasattr(cls, "_PREFECTCH_RELATED_FIELDS"):
      queryset = queryset.prefetch_related(*cls._PREFETCH_RELATED_FIELDS)
    return queryset

class BaseModelSerializer(serializers.ModelSerializer, EagerLoadingMixin):
  pass

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    version = serializers.CharField(max_length=100)

# ICD Serializer
class DiagnosisICDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'



#DiagnosisCategory Seriliazer
class DiagnosisCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCategory
        fields = '__all__'
