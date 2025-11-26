# Data Preservation Strategy for Render Deployment

## Overview
Your Golden Mais application is configured to **PRESERVE ALL ACCOUNT DATA** after deployment to Render. Users can continue logging in with their existing credentials on all subsequent attempts.

---

## ✅ What's Already Protected

### 1. **Database Configuration** (`golden_mais/settings.py`)
- Uses **PostgreSQL on Render** (production) via `DATABASE_URL` environment variable
- Uses **SQLite locally** for development
- **Data persists across deployments** because the database is managed separately by Render

### 2. **Migration Strategy** (`core/migrations/0008_create_default_accounts.py`)
- Uses `get_or_create()` method - **creates accounts ONLY if they don't exist**
- **Never deletes** existing accounts during migration
- Reverse migration does **nothing** (`pass`) to ensure data safety

### 3. **Default Accounts**
```
Admin Account:
  Username: admin
  Password: admin123
  Email: admin@goldenmais.com

Customer Account:
  Username: customer
  Password: customer123
  Email: customer@goldenmais.com
```
These accounts are created once and preserved forever.

### 4. **Render Configuration** (`render.yaml`)
```yaml
startCommand: |
  python manage.py migrate --noinput
  gunicorn golden_mais.wsgi:application
```
- Only runs migrations (never deletes data)
- No `flush`, `reset`, or destructive commands
- Database URL is stored as Render environment variable (separate from code)

---

## 🔒 Data Preservation Guarantees

| Data Type | Preservation Method | Status |
|-----------|-------------------|--------|
| User Accounts | `get_or_create()` migration | ✅ SAFE |
| Customer Profiles | `get_or_create()` migration | ✅ SAFE |
| Products | No deletion in migrations | ✅ SAFE |
| Orders | No deletion in migrations | ✅ SAFE |
| Categories | Migration creates only if missing | ✅ SAFE |
| Sessions | Database-backed sessions | ✅ SAFE |

---

## 📋 Deployment Checklist

Before deploying to Render, ensure:

- [ ] **PostgreSQL database is created** on Render
- [ ] **DATABASE_URL** environment variable is set in Render
- [ ] **SECRET_KEY** environment variable is set in Render
- [ ] **render.yaml** is in the root directory
- [ ] **No custom scripts** that delete data are added
- [ ] **All migrations** use `get_or_create()` or non-destructive operations

---

## 🚀 What Happens During Deployment

1. **Build Phase**
   - Installs dependencies from `requirements.txt`
   - Collects static files

2. **Start Phase** (Data-Safe)
   - Runs `python manage.py migrate --noinput`
     - Creates new tables if missing
     - Adds new columns if needed
     - **Creates default accounts ONLY if they don't exist**
   - Starts Gunicorn web server

3. **Result**
   - All existing accounts remain intact
   - All existing data remains intact
   - Users can log in with their credentials

---

## ⚠️ Critical: What NOT to Do

❌ **Never run these commands in production:**
```bash
python manage.py flush              # DELETES ALL DATA
python manage.py migrate zero       # REVERSES ALL MIGRATIONS
python manage.py sqlflush           # DELETES ALL DATA
```

❌ **Never add these to render.yaml:**
```yaml
python manage.py flush --noinput
python manage.py migrate zero
```

❌ **Never delete migration files** - they're part of your data history

---

## 🔄 How to Add New Features Without Losing Data

When adding new features:

1. **Create new migration** (Django auto-generates)
   ```bash
   python manage.py makemigrations
   ```

2. **Use safe operations:**
   ```python
   # ✅ SAFE - Creates if missing
   MyModel.objects.get_or_create(...)
   
   # ✅ SAFE - Adds new data
   MyModel.objects.create(...)
   
   # ❌ UNSAFE - Deletes data
   MyModel.objects.all().delete()
   ```

3. **Test locally first:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. **Deploy to Render** - data is preserved

---

## 📞 Support

If you accidentally need to reset data:
- Contact Render support to reset the PostgreSQL database
- Or create a new database and update DATABASE_URL
- **But your code will never delete data automatically**

---

## Summary

✅ **Your data is safe because:**
1. Database is managed by Render (separate from code)
2. Migrations use `get_or_create()` (never deletes)
3. No destructive commands in deployment
4. All accounts persist across deployments

**Users can log in with their credentials on 2nd, 3rd, and all subsequent attempts!**
