from django.core.management.base import BaseCommand
from recomender.models import Movie2, Similarity ,Review
from Accounts.models import UserAccount
from django.db import transaction,models
class Command(BaseCommand):
    help = "Copy Movie2, Similarity, and Review objects from default to main DB"

    def copy_movies(self):
        self.stdout.write("Copying Movie2 objects...")
        source_movies = Movie2.objects.using('default').all()
        Movie2.objects.using('main').all().delete()

        for movie in source_movies:
            data = {}
            for field in movie._meta.fields:
                if field.name == 'id':
                    continue

                value = getattr(movie, field.name)

                # Truncate string fields longer than 255 characters
                if isinstance(field, (models.CharField, models.TextField)) and isinstance(value, str):
                    max_length = getattr(field, 'max_length', None)
                    if max_length and len(value) > max_length:
                        value = value[:max_length]

                data[field.name] = value

            try:
                new_movie = Movie2.objects.using('main').create(**data)
                self.stdout.write(f"Copied Movie: {new_movie.title}")
            except Exception as e:
                self.stderr.write(f"Failed to copy movie {movie.id}: {e}")

    def copy_similarities(self):
        self.stdout.write("Copying Similarity objects...")
        source_sims = Similarity.objects.using('default').all()
        Similarity.objects.using('main').all().delete()

        for sim in source_sims:
            try:
                target_movie = Movie2.objects.using('main').get(movie_id=sim.movie.movie_id)
                target_similar_movie = Movie2.objects.using('main').get(movie_id=sim.similar_movie.movie_id)
            except Movie2.DoesNotExist:
                self.stdout.write(f"Skipping Similarity due to missing Movie: {sim.id}")
                continue

            Similarity.objects.using('main').create(movie=target_movie, similar_movie=target_similar_movie)
            self.stdout.write(f"Copied Similarity: {target_movie.title} ~ {target_similar_movie.title}")

    @transaction.atomic(using='main')
    def handle(self, *args, **options):
        self.copy_movies()
        self.copy_similarities()
        self.stdout.write(self.style.SUCCESS("All data copied successfully!"))
