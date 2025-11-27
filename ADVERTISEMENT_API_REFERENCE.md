# Advertisement Management - API Reference

## Overview
This document provides technical details for developers integrating with the Advertisement Management system.

## Model Reference

### Advertisement Model

```python
class Advertisement(models.Model):
    ADVERTISEMENT_TYPES = [
        ('video', 'Video Advertisement'),
        ('banner', 'Banner/Poster'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ]
    
    # Core Fields
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ad_type = models.CharField(max_length=10, choices=ADVERTISEMENT_TYPES)
    
    # Media Fields
    video_file = models.FileField(upload_to='advertisements/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='advertisements/banners/', blank=True, null=True)
    
    # Status & Display
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    display_order = models.PositiveIntegerField(default=0)
    
    # Scheduling
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Metrics
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Methods

#### `is_active_now()`
```python
def is_active_now(self):
    """Check if advertisement should be displayed now"""
    from django.utils import timezone
    now = timezone.now()
    
    if self.status != 'active':
        return False
    
    if self.start_date and now < self.start_date:
        return False
    
    if self.end_date and now > self.end_date:
        return False
    
    return True
```

**Returns**: Boolean - True if ad should be displayed, False otherwise

**Usage**:
```python
ad = Advertisement.objects.get(id=1)
if ad.is_active_now():
    # Display the advertisement
    pass
```

---

## View Functions

### admin_advertisements()
**URL**: `/admin-advertisements/`
**Method**: GET
**Auth Required**: Admin only

**Query Parameters**:
- `type`: Filter by ad type ('video' or 'banner')
- `status`: Filter by status ('draft', 'active', 'inactive', 'archived')
- `page`: Page number for pagination

**Response**: Renders `admin/advertisements.html` with context:
```python
{
    'advertisements': Page object,
    'ad_types': List of (value, label) tuples,
    'statuses': List of (value, label) tuples,
    'current_type_filter': Current type filter or None,
    'current_status_filter': Current status filter or None,
}
```

**Example**:
```
GET /admin-advertisements/?type=video&status=active&page=1
```

---

### admin_advertisement_add()
**URL**: `/admin-advertisement-add/`
**Methods**: GET, POST
**Auth Required**: Admin only

**GET Response**: Renders form template with empty AdvertisementForm

**POST Parameters**:
```python
{
    'title': str (required),
    'description': str (optional),
    'ad_type': str ('video' or 'banner', required),
    'video_file': File (optional, if ad_type='video'),
    'video_url': str (optional, if ad_type='video'),
    'image': File (optional, if ad_type='banner'),
    'status': str (required),
    'display_order': int (optional, default=0),
    'start_date': datetime (optional),
    'end_date': datetime (optional),
}
```

**Success Response**: Redirect to `/admin-advertisements/` with success message

**Error Response**: Re-render form with error messages

---

### admin_advertisement_edit()
**URL**: `/admin-advertisement-edit/<ad_id>/`
**Methods**: GET, POST
**Auth Required**: Admin only
**Parameters**: `ad_id` (integer) - Advertisement ID

**GET Response**: Renders form template with pre-filled AdvertisementForm

**POST Parameters**: Same as `admin_advertisement_add()`

**Success Response**: Redirect to `/admin-advertisements/` with success message

**Error Response**: Re-render form with error messages

---

### admin_advertisement_view()
**URL**: `/admin-advertisement-view/<ad_id>/`
**Method**: GET
**Auth Required**: Admin only
**Parameters**: `ad_id` (integer) - Advertisement ID

**Response**: Renders `admin/advertisement_view.html` with context:
```python
{
    'advertisement': Advertisement object,
}
```

---

### admin_advertisement_delete()
**URL**: `/admin-advertisement-delete/<ad_id>/`
**Methods**: GET, POST
**Auth Required**: Admin only
**Parameters**: `ad_id` (integer) - Advertisement ID

**GET Response**: Renders confirmation template

**POST Response**: Deletes advertisement and redirects to `/admin-advertisements/`

---

### admin_advertisement_toggle_status()
**URL**: `/admin-advertisement-toggle-status/<ad_id>/`
**Method**: POST
**Auth Required**: Admin only
**Parameters**: `ad_id` (integer) - Advertisement ID

**POST Parameters**:
```python
{
    'status': str ('draft', 'active', 'inactive', or 'archived'),
}
```

**Response**: Updates status and redirects to `/admin-advertisements/`

---

## Form Reference

### AdvertisementForm

```python
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'ad_type', 'video_file', 
                  'video_url', 'image', 'status', 'display_order', 
                  'start_date', 'end_date']
```

**Validation Rules**:
- `title`: Required, max 200 characters
- `ad_type`: Required, must be 'video' or 'banner'
- For video ads: Either `video_file` or `video_url` required
- For banner ads: `image` required
- `display_order`: Non-negative integer
- `start_date` and `end_date`: Valid datetime format

**Custom Validation**:
```python
def clean(self):
    # Ensures video ads have video content
    # Ensures banner ads have image
    # Raises ValidationError if validation fails
```

---

## Database Queries

### Common Queries

**Get all active advertisements**:
```python
active_ads = Advertisement.objects.filter(status='active')
```

**Get currently displayable advertisements**:
```python
from django.utils import timezone
now = timezone.now()

displayable_ads = Advertisement.objects.filter(
    status='active',
    start_date__lte=now,
    end_date__gte=now
) | Advertisement.objects.filter(
    status='active',
    start_date__isnull=True,
    end_date__isnull=True
)
```

**Get videos only**:
```python
videos = Advertisement.objects.filter(ad_type='video')
```

**Get banners only**:
```python
banners = Advertisement.objects.filter(ad_type='banner')
```

**Get ordered by display order**:
```python
ordered_ads = Advertisement.objects.all().order_by('display_order', '-created_at')
```

**Get top performing ads**:
```python
top_ads = Advertisement.objects.all().order_by('-views')[:10]
```

**Get recently created**:
```python
recent_ads = Advertisement.objects.all().order_by('-created_at')[:5]
```

---

## File Storage

### Directory Structure
```
media/
└── advertisements/
    ├── videos/
    │   ├── promo_video_1.mp4
    │   ├── summer_sale.webm
    │   └── ...
    └── banners/
        ├── holiday_banner.jpg
        ├── summer_special.png
        └── ...
```

### File Access
```python
# Get file URL
ad = Advertisement.objects.get(id=1)
if ad.video_file:
    video_url = ad.video_file.url  # /media/advertisements/videos/...
if ad.image:
    image_url = ad.image.url  # /media/advertisements/banners/...
```

### File Deletion
Files are automatically deleted when advertisement is deleted (if using FileField with delete=True).

---

## Permissions & Security

### Required Permissions
- All advertisement views require `@admin_required` decorator
- Only staff/admin users can access

### CSRF Protection
- All POST requests require CSRF token
- Token automatically included in forms

### File Validation
- Video formats: MP4, WebM, OGV
- Image formats: JPG, PNG, GIF, WebP
- File size limits enforced at form level

---

## Signals & Hooks

Currently no signals are implemented, but can be added for:
- Auto-generating thumbnails for videos
- Sending notifications when ads go live
- Archiving expired advertisements
- Tracking engagement metrics

**Example signal**:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Advertisement)
def on_advertisement_created(sender, instance, created, **kwargs):
    if created:
        # Send notification to admins
        # Generate thumbnail
        # Log activity
        pass
```

---

## Template Tags & Filters

### Display Active Advertisements
```django
{% for ad in advertisements %}
    {% if ad.is_active_now %}
        <!-- Display advertisement -->
    {% endif %}
{% endfor %}
```

### Format Engagement Metrics
```django
<p>Views: {{ ad.views|intcomma }}</p>
<p>Clicks: {{ ad.clicks|intcomma }}</p>
```

---

## Performance Optimization

### Query Optimization
```python
# Use select_related for foreign keys
ads = Advertisement.objects.select_related('created_by').all()

# Use only() to limit fields
ads = Advertisement.objects.only('title', 'status', 'views')

# Use values() for aggregation
stats = Advertisement.objects.values('ad_type').annotate(
    total_views=Sum('views'),
    total_clicks=Sum('clicks')
)
```

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def admin_advertisements(request):
    # View code
    pass
```

---

## Error Handling

### Common Errors

**Advertisement Not Found**:
```python
from django.http import Http404
try:
    ad = Advertisement.objects.get(id=ad_id)
except Advertisement.DoesNotExist:
    raise Http404("Advertisement not found")
```

**Validation Error**:
```python
from django.core.exceptions import ValidationError
try:
    form = AdvertisementForm(data)
    if not form.is_valid():
        raise ValidationError(form.errors)
except ValidationError as e:
    # Handle error
    pass
```

---

## Testing

### Unit Test Example
```python
from django.test import TestCase
from core.models import Advertisement
from django.contrib.auth.models import User

class AdvertisementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.ad = Advertisement.objects.create(
            title='Test Ad',
            ad_type='banner',
            status='active',
            created_by=self.user
        )
    
    def test_advertisement_creation(self):
        self.assertEqual(self.ad.title, 'Test Ad')
        self.assertEqual(self.ad.status, 'active')
    
    def test_is_active_now(self):
        self.assertTrue(self.ad.is_active_now())
```

---

## Integration Examples

### Display Active Ads on Homepage
```python
# In views.py
def home(request):
    active_ads = Advertisement.objects.filter(
        status='active',
        ad_type='banner'
    ).order_by('display_order')[:5]
    
    context = {
        'advertisements': active_ads,
    }
    return render(request, 'core/home.html', context)
```

### Display Video in Template
```django
{% if ad.video_file %}
    <video width="100%" controls>
        <source src="{{ ad.video_file.url }}" type="video/mp4">
    </video>
{% elif ad.video_url %}
    <iframe src="{{ ad.video_url }}" width="100%" height="400"></iframe>
{% endif %}
```

---

## Changelog

### Version 1.0 (November 2024)
- Initial release
- Video and banner advertisement support
- Status management
- Scheduling with date ranges
- Engagement tracking
- Admin interface

---

## Support

For technical questions or issues, refer to:
- Main documentation: `ADVERTISEMENT_FEATURE_GUIDE.md`
- Implementation details: `ADVERTISEMENT_IMPLEMENTATION_SUMMARY.md`
- Quick start guide: `ADVERTISEMENT_QUICK_START.md`

---

**Last Updated**: November 2024
**API Version**: 1.0
