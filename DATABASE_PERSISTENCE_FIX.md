# Database Persistence Fix for Render Deployment

## Problem
Admin and customer accounts were being deleted after each Render deployment because the application was using SQLite, which is not persistent on Render's free tier.

## Root Cause
- **SQLite Database**: The application was configured to use `db.sqlite3`, a file-based database
- **No Persistence**: Render doesn't persist local files between deployments on the free plan
- **Fresh Database**: Each deployment created a new, empty database, losing all user accounts and data

## Solution
Configured the application to use **PostgreSQL** on Render (persistent) and **SQLite** locally for development.

## Changes Made

### 1. Updated `golden_mais/settings.py`
- Added `dj_database_url` import
- Implemented conditional database configuration:
  - **Production (Render)**: Uses PostgreSQL via `DATABASE_URL` environment variable
  - **Development (Local)**: Uses SQLite for easy local testing

```python
import dj_database_url

if os.getenv('DATABASE_URL'):
    # Production: PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 2. Updated `requirements.txt`
Added two new dependencies:
- `dj-database-url==2.1.0` - Parses DATABASE_URL environment variable
- `psycopg2-binary==2.9.9` - PostgreSQL adapter for Python

## How It Works

### Local Development
- Uses SQLite (`db.sqlite3`)
- No environment variable needed
- Works out of the box

### Render Production
1. Render automatically creates a PostgreSQL database
2. Render sets the `DATABASE_URL` environment variable
3. Django detects `DATABASE_URL` and uses PostgreSQL
4. Data persists across deployments

## Deployment Steps

1. **Push changes to Git**
   ```bash
   git add .
   git commit -m "Add PostgreSQL support for persistent database on Render"
   git push
   ```

2. **Render will automatically:**
   - Install new dependencies from `requirements.txt`
   - Create a PostgreSQL database
   - Set `DATABASE_URL` environment variable
   - Run migrations on the new database
   - Start the application with persistent storage

3. **Verify on Render Dashboard:**
   - Check that PostgreSQL database is created
   - Confirm `DATABASE_URL` is set in environment variables
   - Test login with admin and customer accounts

## Benefits
✅ **Persistent Data**: Accounts survive deployments
✅ **Scalable**: PostgreSQL can handle more data than SQLite
✅ **Production-Ready**: Industry standard for production Django apps
✅ **Local Development**: Still use SQLite locally for convenience
✅ **No Code Changes**: Application works the same way

## Testing After Deployment
1. Deploy to Render
2. Create admin account
3. Create customer account
4. Verify accounts exist after deployment
5. Make a purchase/order
6. Verify data persists after redeployment

## Important Notes
- The `DATABASE_URL` is automatically set by Render
- No manual configuration needed on Render
- Local development continues to work with SQLite
- Migrations will run automatically on first deployment
