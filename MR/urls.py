from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from Accounts.views import login,signup,logout,profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recomender.urls')),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
]
