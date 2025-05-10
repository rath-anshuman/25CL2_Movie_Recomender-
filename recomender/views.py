from django.shortcuts import render
from .recommender_logic import get_recommendations, fetch_poster
from .recommender_logic import movies

def home(request):
    recommended_movies = []
    if request.method == "POST":
        selected_movie = request.POST.get("movie_title")
        results = get_recommendations(selected_movie)
        for _, row in results.iterrows():
            poster_url = fetch_poster(row["movie_id"])
            recommended_movies.append({
                "title": row["title"],
                "poster_url": poster_url
            })
    return render(request, "home.html", {
        "movie_titles": movies["title"].values,
        "recommended_movies": recommended_movies
    })
