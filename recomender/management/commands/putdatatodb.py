# import json
# import requests
# from django.core.management.base import BaseCommand
# from recomender.models import Movie,Movie2

# class Command(BaseCommand):
#     help = "Fetches movie details from TMDB and populates the Movie model"

#     def handle(self, *args, **kwargs):  # Replace with your actual token
#         headers = {
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYzhlMWI4NWE1MWFiMWUxMTQyNzgwZTgzMmVlNDRjYyIsIm5iZiI6MS43NDY4OTk3MzQyMDg5OTk5ZSs5LCJzdWIiOiI2ODFmOTMxNjVhMDEwMDg1NmRhMTU5YmUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EnBFAG8oOQO-wOtM4Hz7vJ_-QiR69tSiULgTpW7rXB0",
#         "Content-Type": "application/json;charset=utf-8"
#     }

#         movie_ids = Movie.objects.values_list('movie_id', flat=True)

#         for movie_id in movie_ids:
#             if Movie2.objects.filter(movie_id=movie_id).exists():
#                 continue  # Skip if already exists

#             url = f"https://api.themoviedb.org/3/movie/{movie_id}"
#             try:
#                 response = requests.get(url, headers=headers)
#                 if response.status_code != 200:
#                     self.stdout.write(self.style.WARNING(f"Failed to fetch movie {movie_id}"))
#                     continue

#                 data = response.json()
#                 collection = data.get('belongs_to_collection') or {}

#                 Movie2.objects.update_or_create(
#                     movie_id=data.get('id'),
#                     defaults={
#                         'imdb_id': data.get('imdb_id'),
#                         'title': data.get('title'),
#                         'original_title': data.get('original_title'),
#                         'overview': data.get('overview'),
#                         'tagline': data.get('tagline'),
#                         'status': data.get('status'),
#                         'adult': data.get('adult', False),
#                         'video': data.get('video', False),
#                         'backdrop_path': data.get('backdrop_path'),
#                         'poster_path': data.get('poster_path'),
#                         'file_path': '',
#                         'budget': data.get('budget', 0),
#                         'revenue': data.get('revenue', 0),
#                         'runtime': data.get('runtime'),
#                         'popularity': data.get('popularity', 0),
#                         'vote_average': data.get('vote_average', 0),
#                         'vote_count': data.get('vote_count', 0),
#                         'homepage': data.get('homepage'),
#                         'release_date': data.get('release_date'),
#                         'original_language': data.get('original_language'),
#                         'genres': json.dumps(data.get('genres', [])),
#                         'spoken_languages': json.dumps(data.get('spoken_languages', [])),
#                         'production_companies': json.dumps(data.get('production_companies', [])),
#                         'production_countries': json.dumps(data.get('production_countries', [])),
#                         'origin_countries': ",".join(data.get('origin_country', [])),
#                         'collection_id': collection.get('id'),
#                         'collection_name': collection.get('name'),
#                         'collection_poster_path': collection.get('poster_path'),
#                         'collection_backdrop_path': collection.get('backdrop_path'),
#                     }
#                 )

#                 self.stdout.write(self.style.SUCCESS(f"Saved movie: {data.get('title')} ({movie_id})"))

#             except Exception as e:
#                 self.stderr.write(f"Error processing movie {movie_id}: {str(e)}")
from recomender.models import Similarity, Movie2, Movie

for sim in Similarity.objects.all():
    try:
        m1 = Movie2.objects.get(movie_id=sim.movie.movie_id)
        m2 = Movie2.objects.get(movie_id=sim.similar_movie.movie_id)

        Similarity.objects.create(
            movie=m1,
            similar_movie=m2,
            score=sim.score
        )
    except Movie2.DoesNotExist:
        continue  # skip if mapping not found
