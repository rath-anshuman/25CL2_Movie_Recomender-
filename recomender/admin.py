from django.contrib import admin

# Register your models here.
from .models import Movie,Similarity

admin.site.register(Movie)
admin.site.register(Similarity)