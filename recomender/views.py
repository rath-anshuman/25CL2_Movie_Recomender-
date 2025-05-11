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
    
    return render(request,'recommendations.html',{'recm':recommendations})

def fetch_tmdb_movie(request,movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYzhlMWI4NWE1MWFiMWUxMTQyNzgwZTgzMmVlNDRjYyIsIm5iZiI6MS43NDY4OTk3MzQyMDg5OTk5ZSs5LCJzdWIiOiI2ODFmOTMxNjVhMDEwMDg1NmRhMTU5YmUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.EnBFAG8oOQO-wOtM4Hz7vJ_-QiR69tSiULgTpW7rXB0",
        "Content-Type": "application/json;charset=utf-8"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # print(data)
        return render(request,'movies.html',{"movie": data})
    except Exception as e:
        return HttpResponse(f"<div>Error fetching movie: {str(e)}</div>")