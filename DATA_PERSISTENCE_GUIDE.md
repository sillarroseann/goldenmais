# Data Persistence Guide for Golden Mais

## Problem
Products added via the admin panel were disappearing after Render deployment.

## Root Cause
Render's free PostgreSQL database can reset, and products weren't being recreated automatically.

## Solution
Created migration `0010_create_default_products.py` that:
- Recreates default products on every deployment
- Uses `get_or_create()` to preserve existing products
- Ensures products are always available

## How It Works

### Migration Chain
1. **0008_create_default_accounts.py** → Creates admin & customer accounts
2. **0009_create_default_categories.py** → Creates product categories
3. **0010_create_default_products.py** → Creates default products ✅ NEW

### Idempotent Behavior
Each migration uses `get_or_create()`:
- **First run**: Creates data if it doesn't exist
- **Subsequent runs**: Finds existing data and preserves it

## Default Products Preserved

The following products will be automatically recreated:

1. **Fresh Sweet Corn (Per Dozen)** - ₱250.00
2. **Grilled Corn Pack (4 pcs)** - ₱180.00
3. **Baby Corn (500g Pack)** - ₱120.00
4. **Family Corn Bundle** - ₱480.00
5. **Snack Pack** - ₱150.00
6. **Corn Lovers Set** - ₱320.00
7. **Sweet Corn** - ₱200.00
8. **Purple Corn** - ₱350.00
9. **Buttered Corn Cups** - ₱80.00

## Adding New Products

### Option 1: Add via Admin Panel (Temporary)
- Products added manually will persist until database reset
- To make them permanent, add to migration 0010

### Option 2: Add to Migration (Permanent)
Edit `core/migrations/0010_create_default_products.py`:
1. Add product data to `products_data` list
2. Run: `python manage.py migrate`
3. Commit and push to Render

### Option 3: Create New Migration
```bash
python manage.py makemigrations --empty core --name add_custom_products
```

Then edit the migration to add your products using `get_or_create()`.

## Deployment Process

After pushing to Render:
```bash
git add .
git commit -m "Add product persistence migration"
git push origin main
```

Render will:
1. Run `python manage.py migrate --noinput`
2. Execute all migrations including 0010
3. Recreate default products if missing
4. Preserve any existing products

## Verification

### Local Testing
```bash
python manage.py migrate
python manage.py shell
>>> from core.models import Product
>>> Product.objects.count()  # Should show 9+ products
```

### After Render Deployment
1. Check Render logs for successful migration
2. Visit `/admin/` and login with `admin` / `admin123`
3. Go to Products section
4. Verify all default products are present

## Important Notes

✅ **Preserved**: Default products from migration
✅ **Preserved**: Products added via admin (until DB reset)
✅ **Preserved**: Product edits and stock updates
⚠️ **Not Preserved**: Products deleted from migration won't be recreated
⚠️ **Note**: If you delete a product in admin, it won't come back until next DB reset

## Render Free Tier Database Limitations

- Free PostgreSQL databases may reset after 90 days of inactivity
- Data is lost when database resets
- **Solution**: Migrations recreate default data automatically

## Recommended Workflow

1. **Add default products** → Add to migration 0010
2. **Add custom products** → Via admin panel (temporary) or new migration (permanent)
3. **Before deployment** → Verify all products in local database
4. **After deployment** → Check Render logs and verify products exist

## Files Modified/Created

- `core/migrations/0010_create_default_products.py` - NEW: Preserves default products
- `core/migrations/0008_create_default_accounts.py` - FIXED: Proper migration API
- `core/migrations/0009_create_default_categories.py` - Already correct
