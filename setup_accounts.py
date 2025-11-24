#!/usr/bin/env python
"""
Script to set up separate admin and customer accounts.
Run with: python manage.py shell < setup_accounts.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'golden_mais.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Customer

# Delete any existing test accounts to start fresh
User.objects.filter(username__in=['admin_ann', 'customer_ann']).delete()

print("=" * 60)
print("SETTING UP SEPARATE ADMIN AND CUSTOMER ACCOUNTS")
print("=" * 60)

# Create Admin Account
print("\n1. Creating Admin Account...")
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
print(f"   ✓ Admin account created:")
print(f"     Username: {admin_user.username}")
print(f"     Email: {admin_user.email}")
print(f"     Password: AdminPass123!")
print(f"     is_staff: {admin_user.is_staff}")
print(f"     is_superuser: {admin_user.is_superuser}")

# Create Customer Account
print("\n2. Creating Customer Account...")
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

print(f"   ✓ Customer account created:")
print(f"     Username: {customer_user.username}")
print(f"     Email: {customer_user.email}")
print(f"     Password: CustomerPass123!")
print(f"     is_staff: {customer_user.is_staff}")
print(f"     Customer Profile: Created")

print("\n" + "=" * 60)
print("ACCOUNT SETUP COMPLETE!")
print("=" * 60)
print("\nADMIN LOGIN:")
print("  URL: https://goldenmais.onrender.com/admin-login/")
print("  Username: admin_ann")
print("  Password: AdminPass123!")

print("\nCUSTOMER LOGIN:")
print("  URL: https://goldenmais.onrender.com/login/")
print("  Username: customer_ann")
print("  Password: CustomerPass123!")

print("\n" + "=" * 60)
print("IMPORTANT: Change these passwords after first login!")
print("=" * 60)
