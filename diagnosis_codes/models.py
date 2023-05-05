from datetime import datetime

from django.db import models


# Abstract base model
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class DiagnosisCategory(BaseModel):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=400)


    def __str__(self):
        return f" (self.code, self.title)"

class IcdVersion(BaseModel):
    version = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=400)


class Diagnosis(BaseModel):
    category = models.ForeignKey(DiagnosisCategory, on_delete=models.DO_NOTHING)
    icd_version = models.ForeignKey(IcdVersion, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=20)
    full_code = models.CharField(max_length=20, unique=True)
    abbreviated_description = models.TextField()
    full_description = models.TextField()

    def __str__(self):
        return self.abbreviated_description
