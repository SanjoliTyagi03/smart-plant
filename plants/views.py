from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Plant


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