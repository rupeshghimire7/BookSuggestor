from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100,null=False, blank=False)

    def __str__(self):
        return self.name[:25]


class Genre(models.Model):
    types = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self) -> str:
        return self.types


class Book(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)
    genre = models.ManyToManyField(Genre)
    author = models.ManyToManyField(Author)
    photo = models.ImageField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name