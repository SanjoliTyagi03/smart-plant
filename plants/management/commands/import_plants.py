import json
import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from plants.models import Plant


class Command(BaseCommand):
    help = 'Delete all existing plants and import from plants.json with images from .temp/'

    def handle(self, *args, **options):
        # Step 1: Delete all existing plants
        # deleted_count = Plant.objects.count()
        # Plant.objects.all().delete()
        # self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing plant(s).'))

        self.stdout.write(self.style.WARNING('Skipping delete existings...'))

        # Step 2: Load plants.json
        json_path = os.path.join(settings.BASE_DIR, 'plants.json')
        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR(f'plants.json not found at: {json_path}'))
            return

        with open(json_path, 'r') as f:
            plants_data = json.load(f)

        temp_dir = os.path.join(settings.BASE_DIR, '.temp')

        # Step 3: Create each plant
        created = 0
        skipped_images = []

        for data in plants_data:
            image_file = data.pop('image_file', None)

            plant = Plant(**data)

            if image_file:
                img_path = os.path.join(temp_dir, image_file)
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as img_f:
                        plant.image.save(image_file, File(img_f), save=False)
                else:
                    skipped_images.append(image_file)
                    self.stdout.write(
                        self.style.WARNING(f'  Image not found, skipping: {image_file}')
                    )

            plant.save()
            created += 1
            self.stdout.write(f'  Created: {plant.name}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done. Created {created} plant(s).'))
        if skipped_images:
            self.stdout.write(
                self.style.WARNING(f'{len(skipped_images)} image(s) were not found in .temp/ and were skipped.')
            )
