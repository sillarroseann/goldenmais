# Generated migration to create and preserve default products

from django.db import migrations
from decimal import Decimal


def create_default_products(apps, schema_editor):
    """Create default products if they don't exist"""
    Category = apps.get_model('core', 'Category')
    Product = apps.get_model('core', 'Product')
    
    # Get or create categories
    fresh_corn_cat, _ = Category.objects.get_or_create(
        slug='fresh-corn',
        defaults={'name': 'Fresh Corn'}
    )
    bundles_cat, _ = Category.objects.get_or_create(
        slug='bundles-combos',
        defaults={'name': 'Bundles & Combos'}
    )
    snacks_cat, _ = Category.objects.get_or_create(
        slug='snacks',
        defaults={'name': 'Snacks'}
    )
    farm_goods_cat, _ = Category.objects.get_or_create(
        slug='farm-goods',
        defaults={'name': 'Farm Goods'}
    )
    
    # Create default products
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
    
    # Create products using get_or_create to preserve them
    for prod_data in products_data:
        Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults=prod_data
        )


def reverse_default_products(apps, schema_editor):
    """Reverse migration - do nothing to preserve products"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_create_default_categories'),
    ]

    operations = [
        migrations.RunPython(create_default_products, reverse_default_products),
    ]
