from django.core.management.base import BaseCommand
from core.models import Product


class Command(BaseCommand):
    help = 'Update existing products with correct images'

    def handle(self, *args, **options):
        # Image mapping for existing products
        image_mapping = {
            'fresh-sweet-corn-per-dozen': 'products/dozenfreshcorn.jpg',
            'grilled-corn-pack-4pcs': 'products/grilledcorn.jpg',
            'baby-corn-500g': 'products/babycorn.jpg',
            'family-corn-bundle': 'products/familycornpack.jpg',
            'snack-pack': 'products/snackpack.jpg',
            'corn-lovers-set': 'products/cornlovers.jpg',
            'sweet-corn': 'products/sweetcorn.jpg',
            'purple-corn': 'products/purplecorn.jpg',
            'buttered-corn-cups': 'products/butteredcorn.jpg',
        }

        updated_count = 0
        
        for slug, image_path in image_mapping.items():
            try:
                product = Product.objects.get(slug=slug)
                product.image = image_path
                product.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated {product.name} with image: {image_path}')
                )
                updated_count += 1
            except Product.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Product with slug "{slug}" not found')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} products with images')
        )
