import os
import psycopg2
import time
from datetime import datetime
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.forms import ModelForm 
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

M2M     = 'M2M'
GCVA    = 'GCVA'
BBBA    = 'BBBA'
TTA     = 'TTA'
CTM     = 'CTM'
MODEL_CHOICES = (
    (M2M, 'M2M'),
    (GCVA, 'GCVA'),
    (BBBA, 'BBBA'),
    (TTA, 'TTA'),
    (CTM, 'CTM'),
)

# ============================================================================================================
# ============================================================================================================
# ============================================================================================================

class Tag(models.Model):
    name            = models.CharField(unique=True, max_length=120)

    class Meta:
        db_table = 'Tag'

    class params:
        db = 'ML'

class ML_Result(models.Model):
    date_run        = models.DateTimeField(auto_now_add=True)
    by_user         = models.CharField(max_length=100, blank=True, null=True)
    ml_type         = models.CharField(max_length=100, blank=True, null=True)
    tags            = models.ManyToManyField(Tag)

    class Meta:
        db_table = 'ML_Result'

    class params:
        db = 'ML'

class S3_File(models.Model):
    name            = models.CharField(unique=True, max_length=120)
    uri             = models.CharField(unique=True, max_length=120)
    ML_Result_fk    = models.ForeignKey(ML_Result, on_delete=models.CASCADE)

    class Meta:
        db_table = 'S3_File'

    class params:
        db = 'ML'


# ============================================================================================================
# ============================================================================================================
# ============================================================================================================

            
