from django.core.management.base import BaseCommand
from plants.models import Plant


class Command(BaseCommand):
    help = 'Add image URLs to all plants in the database'

    def handle(self, *args, **options):
        # High-quality plant images from various sources
        plant_images = {
            'Snake Plant': 'https://images.unsplash.com/photo-1593691509543-c55fb32d8de5?w=500&h=600&fit=crop&auto=format',
            'Pothos': 'https://images.unsplash.com/photo-1586093248292-4e6252f1d5b4?w=500&h=600&fit=crop&auto=format',
            'Spider Plant': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Monstera Deliciosa': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&h=600&fit=crop&auto=format',
            'Peace Lily': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&h=600&fit=crop&auto=format',
            'Rubber Plant': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=600&fit=crop&auto=format',
            'ZZ Plant': 'https://images.unsplash.com/photo-1631377819268-d716cd610cd2?w=500&h=600&fit=crop&auto=format',
            'Fiddle Leaf Fig': 'https://images.unsplash.com/photo-1545239705-1564e58b9e4a?w=500&h=600&fit=crop&auto=format',
            'Aloe Vera': 'https://images.unsplash.com/photo-1509423350716-97f2360af2e4?w=500&h=600&fit=crop&auto=format',
            'Boston Fern': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500&h=600&fit=crop&auto=format',
            'Philodendron Heartleaf': 'https://images.unsplash.com/photo-1586093248292-4e6252f1d5b4?w=500&h=600&fit=crop&auto=format',
            'Dracaena Marginata': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=500&h=600&fit=crop&auto=format',
            'Jade Plant': 'https://images.unsplash.com/photo-1509423350716-97f2360af2e4?w=500&h=600&fit=crop&auto=format',
            'English Ivy': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500&h=600&fit=crop&auto=format',
            'Calathea Orbifolia': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Bird of Paradise': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=500&h=600&fit=crop&auto=format',
            'Pilea Peperomioides': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Anthurium': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&h=600&fit=crop&auto=format',
            'Hoya Carnosa': 'https://images.unsplash.com/photo-1586093248292-4e6252f1d5b4?w=500&h=600&fit=crop&auto=format',
            'Schefflera': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=600&fit=crop&auto=format',
            'Croton': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Parlor Palm': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=500&h=600&fit=crop&auto=format',
            'Dieffenbachia': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Alocasia Amazonica': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Yucca': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=500&h=600&fit=crop&auto=format',
            'Tradescantia Zebrina': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Peperomia Obtusifolia': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Aglaonema': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Maranta Leuconeura': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Haworthia': 'https://images.unsplash.com/photo-1509423350716-97f2360af2e4?w=500&h=600&fit=crop&auto=format',
            'Fittonia': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Monstera Adansonii': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=500&h=600&fit=crop&auto=format',
            'Cactus Prickly Pear': 'https://images.unsplash.com/photo-1509423350716-97f2360af2e4?w=500&h=600&fit=crop&auto=format',
            'Begonia Rex': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Ponytail Palm': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=500&h=600&fit=crop&auto=format',
            'Norfolk Island Pine': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?w=500&h=600&fit=crop&auto=format',
            'String of Hearts': 'https://images.unsplash.com/photo-1586093248292-4e6252f1d5b4?w=500&h=600&fit=crop&auto=format',
            'Oxalis Triangularis': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Caladium': 'https://images.unsplash.com/photo-1572688484438-313a6e50c333?w=500&h=600&fit=crop&auto=format',
            'Lavender': 'https://images.unsplash.com/photo-1611909023032-2d6b3134ecba?w=500&h=600&fit=crop&auto=format',
        }

        updated_count = 0
        for plant_name, image_url in plant_images.items():
            try:
                plant = Plant.objects.get(name=plant_name)
                plant.image_url = image_url
                plant.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Updated image for: {plant.name}')
                )
            except Plant.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Plant not found: {plant_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} plant images!')
        )