import os
import pickle
import django
import gdown

from django.core.management.base import BaseCommand
from django.db import transaction
from recomender.models import Movie, Similarity

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recomender.settings')
django.setup()


class Command(BaseCommand):
    help = 'Populate the database with movie and similarity data from a pickle file'

    def handle(self, *args, **kwargs):
        def load_pickle_from_gdrive():
            file_id = "1n_Qu6EqJERjO21nCeg7_U9zdXOCIi4Ry"
            url = f"https://drive.google.com/uc?id={file_id}"
            cache_path = os.path.join('cache', 'movie_data.pkl')

            os.makedirs('cache', exist_ok=True)

            if not os.path.exists(cache_path):
                self.stdout.write("Downloading pickle from Google Drive...")
                try:
                    gdown.download(url, cache_path, quiet=False)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Failed to download pickle: {e}"))
                    return None, None

            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to load pickle: {e}"))
                return None, None

        # Load data
        movies_df, cosine_sim = load_pickle_from_gdrive()

        if movies_df is None or cosine_sim is None:
            self.stderr.write(self.style.ERROR("Aborting due to errors in loading data."))
            return

        # Remove duplicates and align cosine_sim
        deduped = movies_df.drop_duplicates(subset='movie_id').reset_index()
        original_indices = deduped['index'].tolist()
        movies_df = deduped.drop(columns=['index']).reset_index(drop=True)
        cosine_sim = [cosine_sim[i] for i in original_indices]

        with transaction.atomic():
            self.stdout.write("Clearing existing Movie and Similarity data...")
            Similarity.objects.all().delete()
            Movie.objects.all().delete()

            self.stdout.write("Populating Movie data...")
            movie_objects = {}
            for idx, row in movies_df.iterrows():
                movie_id = row['movie_id']
                title = row['title']
                movie = Movie.objects.create(movie_id=movie_id, title=title)
                movie_objects[idx] = movie

            self.stdout.write("Populating Similarity data...")
            for idx, scores in enumerate(cosine_sim):
                similar_indices = sorted(
                    list(enumerate(scores)), key=lambda x: x[1], reverse=True
                )[1:11]  # Top 10 excluding self

                for i, score in similar_indices:
                    if i in movie_objects:
                        Similarity.objects.create(
                            movie=movie_objects[idx],
                            similar_movie=movie_objects[i],
                            score=score
                        )

        self.stdout.write(self.style.SUCCESS(
            f"Database populated successfully with {len(movie_objects)} movies and {len(movie_objects) * 10} similarities."
        ))
