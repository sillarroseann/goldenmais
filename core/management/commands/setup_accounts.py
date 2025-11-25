from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Customer


class Command(BaseCommand):
    help = 'Ensure default admin and customer accounts exist'

    def handle(self, *args, **options):
        # Create or get admin account
        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@goldenmais.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if admin_created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Admin account created: admin / admin123')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✓ Admin account already exists')
            )

        # Create or get customer account
        customer_user, customer_created = User.objects.get_or_create(
            username='Ann Pedida',
            defaults={
                'email': 'customer@goldenmais.com',
                'first_name': 'Ann',
                'last_name': 'Pedida',
                'is_staff': False,
            }
        )
        
        if customer_created:
            customer_user.set_password('customer123')
            customer_user.save()
            # Create associated Customer object
            Customer.objects.get_or_create(user=customer_user)
            self.stdout.write(
                self.style.SUCCESS('✓ Customer account created: Ann Pedida / customer123')
            )
        else:
            # Ensure Customer object exists
            Customer.objects.get_or_create(user=customer_user)
            self.stdout.write(
                self.style.SUCCESS('✓ Customer account already exists')
            )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Account setup complete!')
        )
