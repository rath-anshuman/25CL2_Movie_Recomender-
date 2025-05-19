from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)  
    file_path = models.CharField(max_length=500, blank=True, null=True)  


class Movie2(models.Model):
    movie_id = models.IntegerField(unique=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    adult = models.BooleanField(default=False)
    video = models.BooleanField(default=False)

    backdrop_path = models.CharField(max_length=500, blank=True, null=True)
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    file_path = models.CharField(max_length=500, blank=True, null=True)

    budget = models.BigIntegerField(default=0)
    revenue = models.BigIntegerField(default=0)
    runtime = models.IntegerField(blank=True, null=True)
    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    homepage = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    original_language = models.CharField(max_length=10, blank=True, null=True)
    
    # Serialized Fields (store as JSON strings or comma-separated)
    genres = models.TextField(blank=True, null=True)  # e.g., '[{"id": 28, "name": "Action"}, ...]'
    spoken_languages = models.TextField(blank=True, null=True)  # e.g., '[{"iso_639_1": "en", ...}]'
    production_companies = models.TextField(blank=True, null=True)
    production_countries = models.TextField(blank=True, null=True)
    origin_countries = models.CharField(max_length=255, blank=True, null=True)  # e.g., 'US,GB'

    # Belongs to Collection (flattened)
    collection_id = models.IntegerField(blank=True, null=True)
    collection_name = models.CharField(max_length=255, blank=True, null=True)
    collection_poster_path = models.CharField(max_length=500, blank=True, null=True)
    collection_backdrop_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title



class Similarity(models.Model):
    movie = models.ForeignKey(Movie2, related_name='base_movie', on_delete=models.CASCADE)
    similar_movie = models.ForeignKey(Movie2, related_name='similar_movies', on_delete=models.CASCADE)

# models.py (in Supabase-powered Django app)
from django.db import models
from Accounts.models import UserAccount
class Review(models.Model):
    movie_id = models.CharField(max_length=100)  # references Movie2.movie_id (not FK)
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE)              # references UserAccount.id (not FK)
    rating = models.IntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def get_movie(self):
        from recomender.models import Movie2
        return Movie2.objects.using('main').get(movie_id=self.movie_id)


