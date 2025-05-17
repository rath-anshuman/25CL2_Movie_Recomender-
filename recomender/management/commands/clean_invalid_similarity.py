from django.core.management.base import BaseCommand
from recomender.models import Similarity, Movie2

class Command(BaseCommand):
    help = 'Deletes invalid Similarity records that reference Movie objects not present in Movie2'

    def handle(self, *args, **kwargs):
        invalid_ids = []

        for s in Similarity.objects.all():
            if not Movie2.objects.filter(movie_id=s.movie.movie_id).exists() or \
               not Movie2.objects.filter(movie_id=s.similar_movie.movie_id).exists():
                invalid_ids.append(s.id)

        count = len(invalid_ids)

        if count == 0:
            self.stdout.write(self.style.SUCCESS("No invalid similarity entries found."))
        else:
            Similarity.objects.filter(id__in=invalid_ids).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {count} invalid Similarity entries."))
