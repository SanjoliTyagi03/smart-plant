from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from .models import BlogPost, Plant
from .gemini import analyze_plant_image


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Choose a username', 'autocomplete': 'username'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder': 'Email address (optional)', 'autocomplete': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create a password', 'autocomplete': 'new-password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'autocomplete': 'new-password'}), label='Confirm Password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        if p1 and len(p1) < 8:
            self.add_error('password1', 'Password must be at least 8 characters.')
        return cleaned


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data.get('email', ''),
            password=form.cleaned_data['password1'],
        )
        login(request, user)
        messages.success(request, f'Welcome, {user.username}! Your account has been created.')
        return redirect('home')
    return render(request, 'plants/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        next_url = request.GET.get('next') or 'home'
        return redirect(next_url)
    return render(request, 'plants/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('home')


def home(request):
    """Landing page with featured plants"""
    featured_plants = Plant.objects.filter(featured=True)[:6]
    context = {
        'featured_plants': featured_plants,
    }
    return render(request, 'plants/home.html', context)


def plant_list(request):
    """Plants list page with search and filters"""
    plants = Plant.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query and search_query.lower() != 'none':
        plants = plants.filter(
            Q(name__icontains=search_query) |
            Q(scientific_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '').strip()
    if difficulty:
        plants = plants.filter(difficulty=difficulty)
    
    # Filter by light requirements
    light = request.GET.get('light', '').strip()
    if light:
        plants = plants.filter(light_requirements=light)
    
    # Filter by pet safe
    pet_safe = request.GET.get('pet_safe')
    if pet_safe == 'true':
        plants = plants.filter(pet_safe=True)
    
    # Filter by air purifying
    air_purifying = request.GET.get('air_purifying')
    if air_purifying == 'true':
        plants = plants.filter(air_purifying=True)
    
    # Clean search query for display
    display_search_query = search_query if search_query and search_query.lower() != 'none' else ''
    
    context = {
        'plants': plants,
        'search_query': display_search_query,
        'selected_difficulty': difficulty,
        'selected_light': light,
        'selected_pet_safe': pet_safe,
        'selected_air_purifying': air_purifying,
        'difficulty_choices': Plant.DIFFICULTY_CHOICES,
        'light_choices': Plant.LIGHT_CHOICES,
    }
    return render(request, 'plants/plant_list.html', context)


def plant_detail(request, pk):
    """Plant detail page with all care information"""
    plant = get_object_or_404(Plant, pk=pk)
    context = {
        'plant': plant,
    }
    return render(request, 'plants/plant_detail.html', context)


@login_required
def analyze(request):
    """Plant analyzer page — upload image, get Gemini health/care report"""
    result = None
    error = None

    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if not image_file:
            error = 'Please upload an image'
        else:
            mime_type = image_file.content_type or 'image/jpeg'
            image_bytes = image_file.read()
            result = analyze_plant_image(image_bytes, mime_type)
            if 'error' in result:
                error = result['error']
                result = None

    return render(request, 'plants/analyze.html', {'result': result, 'error': error})


def about(request):
    return render(request, 'plants/about.html')


def blog_list(request):
    page = request.GET.get('page', 1)
    queryset = BlogPost.objects.all()
    paginator = Paginator(queryset, 9)
    blogs = paginator.get_page(page)
    return render(request, 'plants/blog_list.html', {'blogs': blogs})


def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    recent = BlogPost.objects.exclude(pk=pk).order_by('-created_at')[:3]
    return render(request, 'plants/blog_detail.html', {'blog': blog, 'recent': recent})
