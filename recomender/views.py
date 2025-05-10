# recomender/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, Similarity

def movie_dropdown(request):
    movies = Movie.objects.all()
    return render(request, 'movie_dropdown.html', {'movies': movies})

def get_recommendations_htmx(request):
    movie_id = request.GET.get('movie_id')
    movie = Movie.objects.get(movie_id=movie_id)
    recommendations = Similarity.objects.filter(movie=movie).select_related('similar_movie').order_by('-score')[:10]
    return render(request, 'recommendations.html', {'recommendations': recommendations})
