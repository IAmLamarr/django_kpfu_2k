from django.db import models
from dataclasses import dataclass, field

# Create your models here.

@dataclass
class Post():
    post_id: str
    title: str
    description: str
    text: str
    author: str
    image: str
    keywords: list[str] = field(default_factory=list)
