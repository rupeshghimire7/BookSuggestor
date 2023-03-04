from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# Create your models here.
class Author(models.Model):
    aname = models.CharField(max_length=100,null=False, blank=False)


    def __str__(self):
        return self.aname[:25]


class Genre(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self) -> str:
        return self.type


class Book(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE,default='')
    author = models.ForeignKey(Author,on_delete=models.CASCADE,default='')
    photo = models.ImageField(blank=True,default='media/Hustle.png')

    def __str__(self):
        return self.name
        