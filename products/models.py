from django.db import models
from django.db.models.query_utils import subclasses

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    
class Categories(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    base_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='base_category')