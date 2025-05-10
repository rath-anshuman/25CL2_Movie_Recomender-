import gdown
import os
import pickle
import pandas as pd
from django.shortcuts import render

# Load pickle from Google Drive and cache it
def load_pickle_from_gdrive():
    file_id = "1n_Qu6EqJERjO21nCeg7_U9zdXOCIi4Ry"
    url = f"https://drive.google.com/uc?id={file_id}"
    cache_path = os.path.join('cache', 'movie_data.pkl')

    if not os.path.exists(cache_path):
        os.makedirs('cache', exist_ok=True)
        gdown.download(url, cache_path, quiet=False)

    with open(cache_path, 'rb') as f:
        return pickle.load(f)  # should return movies, cosine_sim

# Load on startup or first use
movies, cosine_sim = load_pickle_from_gdrive()

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

def home(request):
    selected_movie = request.GET.get("movie")
    recommendations = []

    if selected_movie:
        try:
            recommendations = get_recommendations(selected_movie).to_dict(orient='records')
        except:
            recommendations = []

    return render(request, 'home.html', {
        'movies': movies['title'].values,
        'selected_movie': selected_movie,
        'recommendations': recommendations,
    })
