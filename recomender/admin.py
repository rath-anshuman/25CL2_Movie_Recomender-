from django.contrib import admin

# Register your models here.
from .models import Movie,Similarity,Movie2

admin.site.register(Movie)
admin.site.register(Movie2)
admin.site.register(Similarity)