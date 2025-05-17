import os
import pickle
import django
import gdown

from django.core.management.base import BaseCommand
from django.db import transaction
from recomender.models import Movie2, Similarity

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recomender.settings')
django.setup()


class Command(BaseCommand):
    help = 'Populate Similarity table using existing Movie2 data and a precomputed cosine similarity matrix.'

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

        # Deduplicate and align indices
        deduped = movies_df.drop_duplicates(subset='movie_id').reset_index()
        original_indices = deduped['index'].tolist()
        movies_df = deduped.drop(columns=['index']).reset_index(drop=True)
        cosine_sim = [cosine_sim[i] for i in original_indices]

        # Create a map from movie_id to Movie2 instance
        movie_id_to_obj = {m.movie_id: m for m in Movie2.objects.all()}
        movie_idx_to_obj = {}

        # Index Movie2 objects from deduplicated DataFrame
        for idx, row in movies_df.iterrows():
            movie_id = row['movie_id']
            if movie_id in movie_id_to_obj:
                movie_idx_to_obj[idx] = movie_id_to_obj[movie_id]

        with transaction.atomic():
            self.stdout.write("Clearing existing Similarity data...")
            Similarity.objects.all().delete()

            self.stdout.write("Creating Similarity entries...")
            count = 0
            for idx, scores in enumerate(cosine_sim):
                if idx not in movie_idx_to_obj:
                    continue

                main_movie = movie_idx_to_obj[idx]
                similar_indices = sorted(
                    list(enumerate(scores)), key=lambda x: x[1], reverse=True
                )[1:11]  # Top 10

                for i, score in similar_indices:
                    similar_movie = movie_idx_to_obj.get(i)
                    if similar_movie:
                        Similarity.objects.create(
                            movie=main_movie,
                            similar_movie=similar_movie,
                        )
                        count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully added {count} Similarity entries for {len(movie_idx_to_obj)} movies."
        ))
