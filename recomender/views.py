
import json
from django.shortcuts import render,redirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie2, Similarity, Review




def movie_dropdown(request):
    movies = Movie2.objects.using('main').all()
    return render(request, 'movie_dropdown.html', {'movies': movies})


def get_recommendations_htmx(request):
    movie_id = request.GET.get('movie_id')

    try:
        movie = Movie2.objects.using('main').get(movie_id=movie_id)
    except Movie2.DoesNotExist:
        return HttpResponse("<p>Movie not found.</p>")

    recommendations = Similarity.objects.using('main')\
        .filter(movie=movie).select_related('similar_movie')[:10]

    if not recommendations:
        return HttpResponse("<p>No recommendations found.</p>")

    return render(request, 'recommendations.html', {'recm': recommendations})



def fetch_tmdb_movie(request, movie_id):
    data = Movie2.objects.using('main').filter(movie_id=movie_id).first()
    reviews = Review.objects.using('default').filter(movie_id=movie_id).order_by('-created_at')

    if data:
        data.genres = json.loads(data.genres or '[]')
        data.spoken_languages = json.loads(data.spoken_languages or '[]')
        data.production_companies = json.loads(data.production_companies or '[]')
        data.production_countries = json.loads(data.production_countries or '[]')

    return render(request, 'movies.html', {
        "movie": data,
        'reviews': reviews
    })




def submit_review(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        movie_id = request.POST.get("movie_id")  # string ref to Movie2
        review_text = request.POST.get("review")
        rating = request.POST.get("rating")

        Review.objects.create(
            movie_id=movie_id,
            user_id=request.user.id,
            text=review_text,
            rating=rating
        )
        return redirect('movie_detail', movie_id=movie_id)

    return redirect('movie_detail', movie_id=request.GET.get("movie_id"))


       
