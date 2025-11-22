# Golden Mais Commerce Platform

## Overall Concept
Golden Mais is a community-driven commerce platform that connects local farmers in Calubian, Leyte with customers who want fresh, sustainably grown produce. The project blends storytelling pages, a modern product catalog, and responsive checkout experiences so shoppers can discover, customize, and order sweet corn bundles online. Behind the scenes, an internal admin suite keeps orders, inventory, customer messages, and support tickets organized without relying on third-party services.

## Key Features
- **Immersive storefront** – Curated landing, about, and product pages with Tailwind-powered layouts and Font Awesome iconography highlight the Golden Mais brand story.
- **Smart shopping flows** – AJAX add-to-cart, TikTok-style *Buy Now* checkout, cart badges, and mobile-friendly navigation keep shoppers engaged without interruptions.
- **Checkout & payments** – Supports Cash on Delivery/Pickup plus manual GCash/Maya confirmation flows. Real-time payment gateway logic is currently disabled for stability, but the codebase keeps the hooks required for future rollout.
- **Customer engagement** – In-app messaging, feedback forms, and support ticket templates help the team respond quickly while keeping conversations in one place.
- **Operations dashboard** – Custom admin templates for products, orders, feedback, and customers deliver the controls the team needs without exposing the default Django admin look and feel.
- **Responsive experience** – Tailwind CDN, lightweight JavaScript helpers, and semantic templates ensure the site works well on phones, tablets, and desktops.

## Tech Stack
- **Backend:** Django 4.2, SQLite (default dev database)
- **Frontend:** Tailwind CSS CDN, Font Awesome 6, vanilla JS enhancements
- **Media:** Local `media/` storage for uploaded product assets
- **Tooling:** Python virtual environments, `pip`, built-in Django management commands

## Project Layout (highlights)
- `core/` – Django app with models, views, and URLs for storefront + admin experiences
- `templates/` – Public and admin HTML templates (e.g., `templates/core`, `templates/admin`)
- `static/` – Shared static assets and admin-specific overrides
- `payment_settings.py` – Optional configuration stub if payment gateways are reintroduced later
- `RESTORATION_COMPLETE.md` – Notes describing the current stable baseline

## Getting Started
### 1. Prerequisites
- Python 3.11 (or any Python 3.10+ runtime compatible with Django 4.2)
- `pip` and virtual environment tooling (`python -m venv`)

### 2. Installation
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

### 3. Seed essential data
```bash
python manage.py createsuperuser  # optional but recommended for admin access
```

### 4. Run the development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` for the storefront and `/admin/` (or the custom admin URLs) for internal tools.

## Environment & Configuration Notes
- Set `SECRET_KEY`, email credentials, and any SMS/email integration keys via environment variables or `.env` (e.g., using `python-decouple`).
- Static and media paths default to local storage; configure a CDN or object store (S3, etc.) before production deployment.
- Legacy payment gateway credentials are intentionally omitted. If you later restore real-time payments, refresh the keys inside environment variables and re-enable the related code paths.

## Useful Commands
| Purpose            | Command                                   |
|--------------------|-------------------------------------------|
| Run tests          | `python manage.py test`                   |
| Load shell         | `python manage.py shell`                  |
| Collect static     | `python manage.py collectstatic`          |
| Export requirements| `pip freeze > requirements.txt`          |

## Deployment Checklist
1. Configure production-ready settings (`DEBUG=False`, allowed hosts, secure cookies).
2. Point static/media storage to persistent services.
3. Apply migrations & create at least one admin user.
4. Collect static assets and configure your web server (Gunicorn/Uvicorn + Nginx, etc.).
5. Add process supervision (systemd, Supervisor, or container orchestration) and monitoring/backup policies.

## Additional Documentation
- Historical payment gateway helpers remain in `core/payment_service.py` and `payment_settings.py`; treat them as reference only until a new gateway rollout is approved.
