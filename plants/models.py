from django.db import models
from django.urls import reverse


class Plant(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    LIGHT_CHOICES = [
        ('low', 'Low Light'),
        ('medium', 'Medium Light'),
        ('bright', 'Bright Light'),
        ('direct', 'Direct Sunlight'),
    ]
    
    WATER_FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ]

    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL of plant image")
    
    # Care information
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    light_requirements = models.CharField(max_length=10, choices=LIGHT_CHOICES, default='medium')
    water_frequency = models.CharField(max_length=10, choices=WATER_FREQUENCY_CHOICES, default='weekly')
    soil_type = models.CharField(max_length=200, default='Well-draining potting mix')
    temperature_range = models.CharField(max_length=100, default='18-24°C (65-75°F)')
    humidity = models.CharField(max_length=100, default='40-60%')
    
    # Additional care details
    care_instructions = models.TextField(help_text="Detailed care instructions")
    common_problems = models.TextField(blank=True, help_text="Common problems and solutions")
    fertilizer_needs = models.CharField(max_length=200, default='Monthly during growing season')
    repotting_frequency = models.CharField(max_length=100, default='Every 1-2 years')
    
    # Plant characteristics
    mature_size = models.CharField(max_length=100, blank=True)
    growth_rate = models.CharField(max_length=50, default='Medium')
    pet_safe = models.BooleanField(default=False)
    air_purifying = models.BooleanField(default=False)
    is_indoor = models.BooleanField(default=False, help_text="Suitable for indoor growing")
    is_herbal = models.BooleanField(default=False, help_text="Herb / medicinal plant")
    
    # Meta information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_image_url(self):
        """Return image URL, prioritizing uploaded image over URL"""
        if self.image:
            return self.image.url
        return self.image_url

    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    excerpt = models.TextField(blank=True, help_text="Short summary shown on the blog listing page")
    content = models.TextField()
    image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url
