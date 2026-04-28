from django.contrib import admin
from .models import BlogPost, Plant, PlantAnalysis


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'difficulty', 'light_requirements', 'pet_safe', 'air_purifying', 'is_indoor', 'is_herbal', 'featured', 'created_at']
    list_filter = ['difficulty', 'light_requirements', 'pet_safe', 'air_purifying', 'is_indoor', 'is_herbal', 'featured', 'created_at']
    search_fields = ['name', 'scientific_name', 'description']
    list_editable = ['featured', 'pet_safe', 'air_purifying', 'is_indoor', 'is_herbal']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'description', 'image', 'image_url')
        }),
        ('Care Requirements', {
            'fields': ('difficulty', 'light_requirements', 'water_frequency', 'soil_type', 'temperature_range', 'humidity', 'fertilizer_needs', 'repotting_frequency')
        }),
        ('Detailed Care', {
            'fields': ('care_instructions', 'common_problems')
        }),
        ('Plant Characteristics', {
            'fields': ('mature_size', 'growth_rate', 'pet_safe', 'air_purifying', 'is_indoor', 'is_herbal')
        }),
        ('Meta', {
            'fields': ('featured', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'excerpt', 'content']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'excerpt', 'content')
        }),
        ('Image', {
            'fields': ('image', 'image_url')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PlantAnalysis)
class PlantAnalysisAdmin(admin.ModelAdmin):
    list_display = ['plant_name', 'scientific_name', 'health_status', 'user', 'analyzed_at']
    list_filter = ['health_status', 'analyzed_at']
    search_fields = ['plant_name', 'scientific_name', 'user__username']
    readonly_fields = ['analyzed_at']