# Generated migration to create default product categories

from django.db import migrations
from core.models import Category


def create_default_categories(apps, schema_editor):
    """Create default product categories if they don't exist"""
    
    default_categories = [
        {
            'name': 'Fresh Corn',
            'slug': 'fresh-corn',
            'description': 'Fresh, sweet corn directly from our farm'
        },
        {
            'name': 'Snacks',
            'slug': 'snacks',
            'description': 'Delicious corn-based snacks and treats'
        },
        {
            'name': 'Bundles',
            'slug': 'bundles',
            'description': 'Special combo packages and bundles'
        },
        {
            'name': 'Farm Goods',
            'slug': 'farm-goods',
            'description': 'Other farm-fresh products and goods'
        },
        {
            'name': 'Organic',
            'slug': 'organic',
            'description': 'Certified organic corn and products'
        },
        {
            'name': 'Frozen',
            'slug': 'frozen',
            'description': 'Frozen corn and corn products'
        },
    ]
    
    for category_data in default_categories:
        Category.objects.get_or_create(
            slug=category_data['slug'],
            defaults={
                'name': category_data['name'],
                'description': category_data['description'],
            }
        )


def reverse_default_categories(apps, schema_editor):
    """Reverse migration - do nothing to preserve categories"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_create_default_accounts'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, reverse_default_categories),
    ]
