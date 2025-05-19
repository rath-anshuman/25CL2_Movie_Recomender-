from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate, get_user_model,update_session_auth_hash
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from recomender.models import Review,Movie2
User = get_user_model()

@csrf_protect
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            auth_login(request, user)
            return redirect("movie_dropdown")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")
    return render(request, 'account/login.html')

@csrf_protect
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("login")

        user = User.objects.create_user(
            email=email, password=password,
            name=name, age=age, gender=gender
        )
        auth_login(request, user)
        return redirect("movie_dropdown")
    return render(request, 'account/signup.html')

def logout(request):
    auth_logout(request)
    return redirect("profile")

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keeps user logged in
            messages.success(request, "Password updated successfully.")
            return redirect('profile')  # or wherever your profile page is

    return render(request, 'account/profile.html')  # replace with your template

def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    reviews = Review.objects.filter(user_id=request.user.id)
    print(reviews)

    # FIX: convert to int if stored as string
    movie_ids = list(map(int, reviews.values_list('movie_id', flat=True).distinct()))
    print(movie_ids)

    movies = Movie2.objects.using('main').in_bulk(movie_ids, field_name='movie_id')
    print(movies)

    for review in reviews:
        review.movie = movies.get(int(review.movie_id))  # be safe, cast again
        print(review.movie)

    return render(request, "account/profile.html", {
        "user": request.user,
        "reviews": reviews
    })
