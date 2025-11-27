# Advertisement Frontend Integration - Complete Guide

## Overview

The Advertisement Management system is now fully integrated with the customer-facing website. Customers can view promotional banners on the homepage and access a dedicated promotions page with all active video advertisements and banners.

## Frontend Features Implemented

### 1. Homepage Advertisement Section
**Location**: Homepage (`/`)
**Display**: Promotional banners carousel
**Features**:
- Shows up to 5 active banner advertisements
- Displays below the hero section
- Responsive grid layout (1 column on mobile, 3 columns on desktop)
- Hover effects with scale and shadow transitions
- Shows advertisement title and description

### 2. Dedicated Promotions Page
**URL**: `/promotions/`
**Route Name**: `advertisements_page`
**Features**:
- Displays all active video advertisements
- Displays all active banner advertisements
- Organized in separate sections
- Responsive design
- Engagement metrics display (views and dates)
- Call-to-action section for newsletter signup

### 3. Navigation Integration
**Desktop Navigation**: Added "🎯 Promotions" link
**Mobile Navigation**: Added "🎯 Promotions" link
**Placement**: Between Products and Contact links

### 4. API Endpoints (For AJAX/JavaScript)
**Carousel API**: `/api/advertisements/carousel/`
- Returns active banner advertisements in JSON format
- Returns: id, title, image_url, description

**Videos API**: `/api/advertisements/videos/`
- Returns active video advertisements in JSON format
- Returns: id, title, video_url, video_file, description

## File Changes

### Backend Views (`core/views.py`)
1. **Updated `home()` view**
   - Fetches active banner advertisements
   - Filters by status='active' and date range
   - Orders by display_order
   - Passes to template as 'advertisements'

2. **Added `get_active_advertisements()` helper function**
   - Filters advertisements by status and date range
   - Optional type filter (video/banner)
   - Returns ordered queryset

3. **Added `advertisements_carousel()` API view**
   - Returns banner ads as JSON
   - Used for dynamic carousel loading

4. **Added `advertisements_videos()` API view**
   - Returns video ads as JSON
   - Used for dynamic video loading

5. **Added `advertisements_page()` view**
   - Renders dedicated promotions page
   - Fetches both video and banner ads
   - Passes to template

### URLs (`core/urls.py`)
```python
# Main page
path('promotions/', views.advertisements_page, name='advertisements_page'),

# API endpoints
path('api/advertisements/carousel/', views.advertisements_carousel, name='advertisements_carousel'),
path('api/advertisements/videos/', views.advertisements_videos, name='advertisements_videos'),
```

### Templates
1. **`templates/core/home.html`** - Updated
   - Added promotional advertisements section
   - Displays between hero and featured products
   - Responsive grid layout

2. **`templates/core/advertisements.html`** - New
   - Dedicated promotions page
   - Separate sections for videos and banners
   - Engagement metrics display
   - Newsletter signup CTA

3. **`templates/base.html`** - Updated
   - Added "🎯 Promotions" link to desktop navigation
   - Added "🎯 Promotions" link to mobile navigation

## How It Works

### Homepage Flow
1. User visits homepage (`/`)
2. `home()` view executes
3. Fetches active advertisements where:
   - status = 'active'
   - start_date is NULL or <= now
   - end_date is NULL or >= now
   - ad_type = 'banner'
4. Limits to 5 advertisements
5. Orders by display_order
6. Passes to template
7. Template renders promotional section if ads exist

### Promotions Page Flow
1. User clicks "🎯 Promotions" in navigation
2. Navigates to `/promotions/`
3. `advertisements_page()` view executes
4. Fetches active video advertisements
5. Fetches active banner advertisements
6. Renders dedicated page with both types
7. Displays engagement metrics

### API Endpoint Flow
1. JavaScript makes AJAX request to `/api/advertisements/carousel/`
2. View returns JSON with active banners
3. JavaScript processes and displays dynamically
4. Same for video endpoint

## Display Logic

### Active Advertisement Criteria
An advertisement is displayed if:
1. **Status**: Must be 'active'
2. **Start Date**: 
   - If set: Current time must be >= start_date
   - If not set: No restriction
3. **End Date**:
   - If set: Current time must be <= end_date
   - If not set: No restriction
4. **Type**: Must match the requested type (video/banner)

### Example Scenarios

**Scenario 1: Always Active Banner**
```
Status: Active
Start Date: (empty)
End Date: (empty)
Result: Always displayed
```

**Scenario 2: Limited Time Promotion**
```
Status: Active
Start Date: Dec 1, 2024 00:00
End Date: Dec 31, 2024 23:59
Result: Only displayed during December 2024
```

**Scenario 3: Upcoming Campaign**
```
Status: Active
Start Date: Jan 1, 2025 00:00
End Date: (empty)
Result: Displayed from Jan 1, 2025 onwards
```

**Scenario 4: Expired Campaign**
```
Status: Active
Start Date: (empty)
End Date: Nov 30, 2024 23:59
Result: Not displayed (date has passed)
```

## Responsive Design

### Desktop (lg screens)
- Homepage: 3 columns grid
- Promotions page: 2 columns for videos, 3 columns for banners

### Tablet (md screens)
- Homepage: 2 columns grid
- Promotions page: 2 columns for videos, 2 columns for banners

### Mobile (sm screens)
- Homepage: 1 column grid
- Promotions page: 1 column for both videos and banners

## Styling

### Colors Used
- **Background**: Yellow-100 to Green-100 gradient
- **Text**: Green-700 for headings
- **Accents**: Yellow-500 for icons
- **Hover**: Scale 1.05 with shadow increase

### CSS Classes
- `rounded-xl`: Rounded corners
- `shadow-lg`: Box shadow
- `hover:shadow-2xl`: Hover shadow effect
- `transition`: Smooth transitions
- `transform hover:scale-105`: Hover scale effect

## Performance Considerations

### Database Queries
- Uses Django ORM with proper filtering
- Limits results (5 on homepage, unlimited on promotions page)
- Orders by display_order for consistency

### Caching Opportunities
```python
# Can be added later for optimization
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def advertisements_page(request):
    # View code
```

### Image Optimization
- Images should be compressed before upload
- Recommended sizes:
  - Homepage banners: 600x300px (will be displayed at 1200x400px)
  - Promotions page: 1200x400px

## User Experience

### Homepage
- Advertisements appear prominently below hero section
- Encourages users to explore promotions
- Drives engagement with special offers

### Promotions Page
- Dedicated space for all promotions
- Separate sections for videos and banners
- Clear call-to-action for newsletter signup
- Engagement metrics show popularity

### Navigation
- Easy access from main menu
- Emoji icon (🎯) makes it visually distinct
- Available on both desktop and mobile

## Testing Checklist

- [x] Homepage displays advertisements section
- [x] Promotions page loads correctly
- [x] Navigation links work
- [x] Responsive design on all screen sizes
- [x] Active advertisements filter works
- [x] Date range filtering works
- [x] API endpoints return correct JSON
- [x] No advertisements message displays when empty
- [x] Hover effects work smoothly
- [x] Images display correctly

## Future Enhancements

1. **Dynamic Carousel**
   - Auto-rotate advertisements
   - Previous/Next buttons
   - Pagination indicators

2. **Video Player Enhancements**
   - Custom video player
   - Thumbnail previews
   - Auto-play on scroll

3. **Analytics**
   - Track advertisement views
   - Track clicks
   - Display engagement metrics

4. **Search & Filter**
   - Filter by date range
   - Search by title
   - Sort by popularity

5. **Notifications**
   - Email notifications for new promotions
   - Push notifications
   - In-app notifications

## Troubleshooting

### Advertisements Not Showing

**Check 1: Status**
- Verify advertisement status is 'active'
- Go to admin panel and check

**Check 2: Date Range**
- Check if current date is within start/end dates
- Verify server time is correct

**Check 3: Type**
- Homepage only shows 'banner' type
- Promotions page shows both types

**Check 4: Database**
- Verify advertisements exist in database
- Check migration was applied

### Images Not Displaying

**Check 1: File Upload**
- Verify file was uploaded successfully
- Check media directory permissions

**Check 2: File Path**
- Verify image URL is correct
- Check static files are served

**Check 3: File Format**
- Verify file is supported format (JPG, PNG, GIF)
- Check file is not corrupted

### Videos Not Playing

**Check 1: Video File**
- Verify video format is supported (MP4, WebM, OGV)
- Check video file is not corrupted

**Check 2: Video URL**
- Verify URL is correct and accessible
- Check external video service is available

**Check 3: Browser**
- Try different browser
- Check browser supports video format

## API Documentation

### GET /api/advertisements/carousel/

**Response**:
```json
{
  "advertisements": [
    {
      "id": 1,
      "title": "Summer Sale",
      "image_url": "/media/advertisements/banners/summer.jpg",
      "description": "50% off on all corn products"
    }
  ]
}
```

### GET /api/advertisements/videos/

**Response**:
```json
{
  "advertisements": [
    {
      "id": 2,
      "title": "How to Cook Corn",
      "video_url": "https://youtube.com/watch?v=...",
      "video_file": null,
      "description": "Learn the best ways to cook fresh corn"
    }
  ]
}
```

## Deployment Notes

1. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

2. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Test URLs**
   - Visit `/` - Check homepage ads
   - Visit `/promotions/` - Check promotions page
   - Visit `/api/advertisements/carousel/` - Check API

4. **Verify Media Files**
   - Check media directory is writable
   - Check uploaded files are accessible

## Support

For issues or questions:
1. Check troubleshooting section
2. Review admin panel for advertisement status
3. Check server logs for errors
4. Contact development team

---

**Last Updated**: November 2024
**Version**: 1.0
**Status**: Production Ready
