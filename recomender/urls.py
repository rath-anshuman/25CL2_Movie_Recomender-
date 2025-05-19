# recomender/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_dropdown, name='movie_dropdown'),
    path('get_recommendations/', views.get_recommendations_htmx, name='get_recommendations_htmx'),
    path('movie/<int:movie_id>/', views.fetch_tmdb_movie, name='movie_detail'),
    path('movies/review/', views.submit_review, name='submit_review'),
]

