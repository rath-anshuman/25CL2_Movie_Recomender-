# recomender/views.py
import requests

from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, Similarity
from django.template.loader import render_to_string

def movie_dropdown(request):
    movies = Movie.objects.all()
    return render(request, 'movie_dropdown.html', {'movies': movies})

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Movie, Similarity

def get_recommendations_htmx(request):
    movie_id = request.GET.get('movie_id')

    try:
        movie = Movie.objects.get(movie_id=movie_id)
    except Movie.DoesNotExist:
        return HttpResponse("<p>Movie not found.</p>")

    recommendations = Similarity.objects.filter(movie=movie).select_related('similar_movie').order_by('-score')[:10]

    if not recommendations:
        return HttpResponse("<p>No recommendations found.</p>")

    tmdb_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYzhlMWI4NWE1MWFiMWUxMTQyNzgwZTgzMmVlNDRjYyIsIm5iZiI6MS43NDY4OTk3MzQyMDg5OTk5ZSs5LCJzdWIiOiI2ODFmOTMxNjVhMDEwMDg1NmRhMTU5YmUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EnBFAG8oOQO-wOtM4Hz7vJ_-QiR69tSiULgTpW7rXB0"  # Replace this with your TMDB token
    headers = {
        "Authorization": tmdb_token,
        "Content-Type": "application/json;charset=utf-8"
    }

    html = f"""
    <h2 style="grid-column: 1 / -1; text-align: center; margin-bottom: 20px;">
        Because you like {movie.title}, you might also enjoy:
    </h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">
    """

    for rec in recommendations:
        similar = rec.similar_movie
        tmdb_url = f"https://api.themoviedb.org/3/movie/{similar.movie_id}"
        try:
            res = requests.get(tmdb_url, headers=headers)
            data = res.json()
            poster_path = data.get("poster_path")
            overview = data.get("overview", "No description available.")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"

            html += f"""
            <div class="movie-card" style="border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <img src="{poster_url}" alt="{similar.title}" style="width: 100%; height: auto;">
                <div class="movie-info" style="padding: 10px;">
                    <h3 style="margin: 0 0 10px;">{similar.title}</h3>
                    <p style="font-size: 14px; color: #333;">{overview[:200]}...</p>
                </div>
            </div>
            """
        except Exception as e:
            html += f"<div>Error fetching data for movie ID {similar.movie_id}: {e}</div>"

    html += "</div>"
    return HttpResponse(html)

def fetch_tmdb_movie(request,movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYzhlMWI4NWE1MWFiMWUxMTQyNzgwZTgzMmVlNDRjYyIsIm5iZiI6MS43NDY4OTk3MzQyMDg5OTk5ZSs5LCJzdWIiOiI2ODFmOTMxNjVhMDEwMDg1NmRhMTU5YmUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EnBFAG8oOQO-wOtM4Hz7vJ_-QiR69tSiULgTpW7rXB0",
        "Content-Type": "application/json;charset=utf-8"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        html = render_to_string("partials/tmdb_movie_card.html", {"movie": data})
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<div>Error fetching movie: {str(e)}</div>")