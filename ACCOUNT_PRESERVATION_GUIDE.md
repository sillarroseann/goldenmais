# Account Preservation Guide for Golden Mais

## Problem Fixed ✅

The migration `0008_create_default_accounts.py` was using direct imports instead of `apps.get_model()`, which could cause issues during deployment.

## Solution Applied

Updated the migration to use Django's proper migration API:
- Changed from: `from django.contrib.auth.models import User`
- Changed to: `User = apps.get_model('auth', 'User')`

This ensures the migration works correctly across all environments (local, Render, etc.).

## How Account Preservation Works

### Migration: `0008_create_default_accounts.py`

The migration uses `get_or_create()` which is **idempotent** (safe to run multiple times):

```python
User.objects.get_or_create(
    username='admin',
    defaults={...}
)
```

**Behavior:**
- **First run**: User doesn't exist → Create it with password
- **Subsequent runs**: User exists → Do nothing (preserve it)

### Deployment Process (Render)

1. `render.yaml` runs: `python manage.py migrate --noinput`
2. Migration 0008 executes
3. Checks if `admin` user exists
4. If exists → Preserves it
5. If not exists → Creates it

## Default Accounts

After deployment, these accounts are available:

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@goldenmais.com`
- **Access**: Admin dashboard at `/admin/`

### Customer Account
- **Username**: `customer`
- **Password**: `customer123`
- **Email**: `customer@goldenmais.com`
- **Access**: Customer pages at `/`

## Verification Steps

### Local Testing
```bash
# Run migrations locally
python manage.py migrate

# Check if accounts were created
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username__in=['admin', 'customer'])
```

### After Render Deployment
1. Go to your Render dashboard
2. Check deployment logs for migration output
3. Try logging in with:
   - Admin: `admin` / `admin123`
   - Customer: `customer` / `customer123`

## Important Notes

- ✅ Accounts are **preserved** across deployments
- ✅ Passwords are **never changed** after first creation
- ✅ Customer profiles are **automatically created**
- ✅ The reverse migration does nothing (safe)
- ⚠️ Do NOT manually delete these accounts in the database

## If Accounts Still Don't Exist

If accounts are missing after deployment:

1. **Check Render logs** for migration errors
2. **Verify database connection** in Render dashboard
3. **Check DATABASE_URL** environment variable is set
4. **Run migration manually** (if possible):
   ```bash
   python manage.py migrate 0008
   ```

## Additional Security Notes

For production (Render):
- Change the default passwords immediately after first login
- Consider using environment variables for credentials
- Implement additional authentication methods (2FA, etc.)

## Files Modified

- `core/migrations/0008_create_default_accounts.py` - Fixed to use `apps.get_model()`
