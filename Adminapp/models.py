from django.db import models

class CategoryDb(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)

class SubCategoryDb(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)
    subcategory_name = models.CharField(max_length=100, null=True, blank=True)

