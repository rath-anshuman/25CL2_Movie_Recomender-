import csv
from django.core.management.base import BaseCommand
from recomender.models import Movie2, Similarity
from django.utils.timezone import is_naive, make_naive

class Command(BaseCommand):
    help = "Export Movie2 and Similarity data to CSV for Supabase"

    def handle(self, *args, **options):
        self.export_movies()
        self.export_similarities()

    def export_movies(self):
        file_path = 'movie2_export.csv'
        fields = [field.name for field in Movie2._meta.fields]

        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)

            for obj in Movie2.objects.all():
                row = []
                for field in fields:
                    value = getattr(obj, field)
                    # Convert datetime/date to string
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    row.append(value)
                writer.writerow(row)

        self.stdout.write(f"✅ Movie2 exported to {file_path}")

    def export_similarities(self):
        file_path = 'similarity_export.csv'

        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'movie_id', 'similar_movie_id'])

            for s in Similarity.objects.all():
                writer.writerow([s.id, s.movie_id, s.similar_movie_id])

        self.stdout.write(f"✅ Similarity exported to {file_path}")
