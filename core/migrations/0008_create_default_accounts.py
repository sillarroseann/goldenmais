# Generated migration to create and preserve default admin and customer accounts

from django.db import migrations


def create_default_accounts(apps, schema_editor):
    """Create default admin and customer accounts if they don't exist"""
    from django.contrib.auth.hashers import make_password
    
    User = apps.get_model('auth', 'User')
    Customer = apps.get_model('core', 'Customer')
    
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create(
            username='admin',
            email='admin@goldenmais.com',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            password=make_password('admin123')
        )
    
    # Create default customer user if it doesn't exist
    if not User.objects.filter(username='customer').exists():
        customer_user = User.objects.create(
            username='customer',
            email='customer@goldenmais.com',
            first_name='Customer',
            last_name='User',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            password=make_password('customer123')
        )
        # Create customer profile for the customer user
        Customer.objects.get_or_create(
            user=customer_user,
            defaults={
                'phone': '',
                'address': '',
                'city': '',
            }
        )
    else:
        # Ensure customer profile exists for existing customer user
        customer_user = User.objects.get(username='customer')
        Customer.objects.get_or_create(user=customer_user)


def reverse_default_accounts(apps, schema_editor):
    """Reverse migration - do nothing to preserve accounts"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_product_category'),
    ]

    operations = [
        migrations.RunPython(create_default_accounts, reverse_default_accounts),
    ]
