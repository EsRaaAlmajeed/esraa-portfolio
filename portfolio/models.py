from django.db import models
from django.utils.text import slugify

# Create your models here.
class Project (models.Model):
    title= models.CharField (max_length=200)
    slug= models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    github_url = models.URLField()
    live_url = models.URLField(blank=True)
     
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
     
     
    def __str__(self):
             return self.name