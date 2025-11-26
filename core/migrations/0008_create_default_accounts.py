# Generated migration to create and preserve default admin and customer accounts

from django.db import migrations


def create_default_accounts(apps, schema_editor):
    """Create default admin and customer accounts if they don't exist"""
    User = apps.get_model('auth', 'User')
    Customer = apps.get_model('core', 'Customer')
    
    # Create admin user if it doesn't exist
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@goldenmais.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    # Create default customer user if it doesn't exist
    customer_user, created = User.objects.get_or_create(
        username='customer',
        defaults={
            'email': 'customer@goldenmais.com',
            'first_name': 'Customer',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
        }
    )
    if created:
        customer_user.set_password('customer123')
        customer_user.save()
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
