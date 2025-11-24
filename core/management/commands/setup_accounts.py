from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Customer


class Command(BaseCommand):
    help = 'Set up separate admin and customer accounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('SETTING UP SEPARATE ADMIN AND CUSTOMER ACCOUNTS'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Create Admin Account (only if it doesn't exist)
        self.stdout.write('\n1. Checking Admin Account...')
        admin_user, admin_created = User.objects.get_or_create(
            username='admin_ann',
            defaults={
                'email': 'admin@goldenmais.com',
                'first_name': 'Ann',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if admin_created:
            admin_user.set_password('AdminPass123!')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('   ✓ Admin account CREATED:'))
            self.stdout.write(f'     Username: {admin_user.username}')
            self.stdout.write(f'     Email: {admin_user.email}')
            self.stdout.write(f'     Password: AdminPass123!')
        else:
            self.stdout.write(self.style.WARNING('   ℹ Admin account already exists (not modified):'))
            self.stdout.write(f'     Username: {admin_user.username}')
            self.stdout.write(f'     Email: {admin_user.email}')

        # Create Customer Account (only if it doesn't exist)
        self.stdout.write('\n2. Checking Customer Account...')
        customer_user, customer_created = User.objects.get_or_create(
            username='customer_ann',
            defaults={
                'email': 'customer@goldenmais.com',
                'first_name': 'Ann',
                'last_name': 'Customer',
                'is_staff': False,
                'is_superuser': False,
                'is_active': True
            }
        )

        if customer_created:
            customer_user.set_password('CustomerPass123!')
            customer_user.save()
            
            # Create customer profile
            customer_profile, _ = Customer.objects.get_or_create(
                user=customer_user,
                defaults={
                    'phone': '09123456789',
                    'address': 'Sample Address',
                    'city': 'Manila'
                }
            )
            
            self.stdout.write(self.style.SUCCESS('   ✓ Customer account CREATED:'))
            self.stdout.write(f'     Username: {customer_user.username}')
            self.stdout.write(f'     Email: {customer_user.email}')
            self.stdout.write(f'     Password: CustomerPass123!')
            self.stdout.write(f'     Customer Profile: Created')
        else:
            self.stdout.write(self.style.WARNING('   ℹ Customer account already exists (not modified):'))
            self.stdout.write(f'     Username: {customer_user.username}')
            self.stdout.write(f'     Email: {customer_user.email}')

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('ACCOUNT SETUP COMPLETE!'))
        self.stdout.write('=' * 60)

        self.stdout.write('\nADMIN LOGIN:')
        self.stdout.write('  URL: https://goldenmais.onrender.com/admin-login/')
        self.stdout.write('  Username: admin_ann')
        self.stdout.write('  Password: AdminPass123!')

        self.stdout.write('\nCUSTOMER LOGIN:')
        self.stdout.write('  URL: https://goldenmais.onrender.com/login/')
        self.stdout.write('  Username: customer_ann')
        self.stdout.write('  Password: CustomerPass123!')

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.WARNING('IMPORTANT: Change these passwords after first login!'))
        self.stdout.write('=' * 60)
