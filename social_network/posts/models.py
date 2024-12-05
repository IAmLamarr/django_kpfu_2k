from django.db import models
from dataclasses import dataclass, field
from uuid import uuid4
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True

class Keyword(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True
    )

class Post(BaseModel):
    title = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField()
    text = models.TextField()
    # author
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
    )
    image = models.ImageField(storage=fs)
