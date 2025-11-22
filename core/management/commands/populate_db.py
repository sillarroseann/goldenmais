from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from core.models import Category, Product


class Command(BaseCommand):
    help = 'Populate database with clean data (no demo content)'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Fresh Corn', 'slug': 'fresh-corn'},
            {'name': 'Bundles & Combos', 'slug': 'bundles-combos'},
            {'name': 'Snacks', 'slug': 'snacks'},
            {'name': 'Farm Goods', 'slug': 'farm-goods'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get categories
        fresh_corn_cat = Category.objects.get(slug='fresh-corn')
        bundles_cat = Category.objects.get(slug='bundles-combos')
        snacks_cat = Category.objects.get(slug='snacks')
        farm_goods_cat = Category.objects.get(slug='farm-goods')

        # Create products
        products_data = [
            {
                'name': 'Fresh Sweet Corn (Per Dozen)',
                'slug': 'fresh-sweet-corn-per-dozen',
                'description': 'Naturally sweet, freshly picked corn from our farm — perfect for any meal.',
                'price': Decimal('250.00'),
                'category': fresh_corn_cat,
                'product_type': 'fresh-corn',
                'is_featured': True,
                'is_new': True,
                'stock_quantity': 50,
                'image': 'products/dozenfreshcorn.jpg',
            },
            {
                'name': 'Grilled Corn Pack (4 pcs)',
                'slug': 'grilled-corn-pack-4pcs',
                'description': 'Smoky, buttery grilled corn ready to eat — your favorite street-style treat!',
                'price': Decimal('180.00'),
                'category': snacks_cat,
                'product_type': 'snacks',
                'is_bestseller': True,
                'stock_quantity': 30,
                'image': 'products/grilledcorn.jpg',
            },
            {
                'name': 'Baby Corn (500g Pack)',
                'slug': 'baby-corn-500g',
                'description': 'Crunchy baby corn ideal for salads, stir-fries, and healthy snacking.',
                'price': Decimal('120.00'),
                'category': farm_goods_cat,
                'product_type': 'farm-goods',
                'free_delivery': True,
                'stock_quantity': 25,
                'image': 'products/babycorn.jpg',
            },
            {
                'name': 'Family Corn Bundle',
                'slug': 'family-corn-bundle',
                'description': '10 cobs + butter sachets — perfect for sharing!',
                'price': Decimal('480.00'),
                'category': bundles_cat,
                'product_type': 'bundles',
                'is_featured': True,
                'free_delivery': True,
                'stock_quantity': 15,
                'image': 'products/familycornpack.jpg',
            },
            {
                'name': 'Snack Pack',
                'slug': 'snack-pack',
                'description': 'Sweet corn kernels + seasoning — your quick comfort snack.',
                'price': Decimal('150.00'),
                'category': snacks_cat,
                'product_type': 'snacks',
                'stock_quantity': 40,
                'image': 'products/snackpack.jpg',
            },
            {
                'name': 'Corn Lovers Set',
                'slug': 'corn-lovers-set',
                'description': '5 cobs + homemade butter + chili flakes for a gourmet treat.',
                'price': Decimal('320.00'),
                'category': bundles_cat,
                'product_type': 'bundles',
                'is_bestseller': True,
                'stock_quantity': 20,
                'image': 'products/cornlovers.jpg',
            },
            {
                'name': 'Sweet Corn',
                'slug': 'sweet-corn',
                'description': 'Classic favorite, harvested fresh for peak sweetness and crunch.',
                'price': Decimal('200.00'),
                'category': fresh_corn_cat,
                'product_type': 'fresh-corn',
                'is_featured': True,
                'stock_quantity': 60,
                'image': 'products/sweetcorn.jpg',
            },
            {
                'name': 'Purple Corn',
                'slug': 'purple-corn',
                'description': 'Rare and premium — rich in antioxidants and full-bodied flavor.',
                'price': Decimal('350.00'),
                'category': fresh_corn_cat,
                'product_type': 'fresh-corn',
                'stock_quantity': 10,
                'image': 'products/purplecorn.jpg',
            },
            {
                'name': 'Buttered Corn Cups',
                'slug': 'buttered-corn-cups',
                'description': 'Sweet, buttery, and creamy corn cups for your quick snack cravings.',
                'price': Decimal('80.00'),
                'category': snacks_cat,
                'product_type': 'snacks',
                'stock_quantity': 35,
                'image': 'products/butteredcorn.jpg',
            },
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@goldenmais.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with products and categories!'))
        self.stdout.write('The website is ready for real customers to register and use.')
