# recomender/views.py
import requests

from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie2, Similarity
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
        movie = Movie2.objects.get(movie_id=movie_id)
    except Movie.DoesNotExist:
        return HttpResponse("<p>Movie not found.</p>")

    recommendations = Similarity.objects.filter(movie=movie).select_related('similar_movie')[:10]

    if not recommendations:
        return HttpResponse("<p>No recommendations found.</p>")
    
    return render(request,'recommendations.html',{'recm':recommendations})

import json
def fetch_tmdb_movie(request,movie_id):
    data = Movie2.objects.filter(movie_id=movie_id).first()
    reviews = Review.objects.filter(movie=data).order_by('-created_at')
    if data:
        # Parse JSON fields
        data.genres = json.loads(data.genres or '[]')
        data.spoken_languages = json.loads(data.spoken_languages or '[]')
        data.production_companies = json.loads(data.production_companies or '[]')
        data.production_countries = json.loads(data.production_countries or '[]')

    return render(request, 'movies.html', {"movie": data,'reviews': reviews})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie2, Review


def submit_review(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")  # corrected here
        movie = get_object_or_404(Movie2, movie_id=movie_id)
        review_text = request.POST.get("review")
        rating = request.POST.get("rating")

        Review.objects.create(
            movie=movie,
            user=request.user,
            text=review_text,
            rating=rating
        )
        return redirect('movie_detail', movie_id=movie_id)
    
    # fallback for GET or other methods
    return redirect('movie_detail', movie_id=request.GET.get("movie_id"))


       
