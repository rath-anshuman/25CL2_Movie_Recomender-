from django.db import models

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)

class Similarity(models.Model):
    movie = models.ForeignKey(Movie, related_name='similarities', on_delete=models.CASCADE)
    similar_movie = models.ForeignKey(Movie, related_name='+', on_delete=models.CASCADE)
    score = models.FloatField()
