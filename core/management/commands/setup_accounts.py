from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Customer


class Command(BaseCommand):
    help = 'Set up separate admin and customer accounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('SETTING UP SEPARATE ADMIN AND CUSTOMER ACCOUNTS'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Delete any existing test accounts to start fresh
        User.objects.filter(username__in=['admin_ann', 'customer_ann']).delete()

        # Create Admin Account
        self.stdout.write('\n1. Creating Admin Account...')
        admin_user = User.objects.create_user(
            username='admin_ann',
            email='admin@goldenmais.com',
            password='AdminPass123!',
            first_name='Ann',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS('   ✓ Admin account created:'))
        self.stdout.write(f'     Username: {admin_user.username}')
        self.stdout.write(f'     Email: {admin_user.email}')
        self.stdout.write(f'     Password: AdminPass123!')
        self.stdout.write(f'     is_staff: {admin_user.is_staff}')
        self.stdout.write(f'     is_superuser: {admin_user.is_superuser}')

        # Create Customer Account
        self.stdout.write('\n2. Creating Customer Account...')
        customer_user = User.objects.create_user(
            username='customer_ann',
            email='customer@goldenmais.com',
            password='CustomerPass123!',
            first_name='Ann',
            last_name='Customer',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        # Create customer profile
        customer_profile = Customer.objects.create(
            user=customer_user,
            phone='09123456789',
            address='Sample Address',
            city='Manila'
        )

        self.stdout.write(self.style.SUCCESS('   ✓ Customer account created:'))
        self.stdout.write(f'     Username: {customer_user.username}')
        self.stdout.write(f'     Email: {customer_user.email}')
        self.stdout.write(f'     Password: CustomerPass123!')
        self.stdout.write(f'     is_staff: {customer_user.is_staff}')
        self.stdout.write(f'     Customer Profile: Created')

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
