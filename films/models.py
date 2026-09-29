from django.db import models


# Create your models here.

class Film(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    is_hit = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
