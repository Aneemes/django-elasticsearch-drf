from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
    	Category, related_name='category', on_delete=models.CASCADE
    	)