from django.db import models


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def fio(self):
        return self.__str__()


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Film(models.Model):
    genres = models.ManyToManyField(Genre)
    director = models.ForeignKey(Director, on_delete=models.CASCADE,
                                 null=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField()
    is_hit = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


STARS = ((i, i) for i in range(1, 11))


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=7)
    film = models.ForeignKey(Film, on_delete=models.CASCADE,
                             related_name='reviews')

    def __str__(self):
        return self.text
