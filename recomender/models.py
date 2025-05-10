from django.db import models

from django.db import models

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)  # Add this
    file_path = models.CharField(max_length=500, blank=True, null=True)  # Add this


class Similarity(models.Model):
    movie = models.ForeignKey(Movie, related_name='similarities', on_delete=models.CASCADE)
    similar_movie = models.ForeignKey(Movie, related_name='sim', on_delete=models.CASCADE)
    score = models.FloatField()
