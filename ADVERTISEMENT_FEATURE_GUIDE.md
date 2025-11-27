# Advertisement Management Feature Guide

## Overview

The Advertisement Management feature allows admins to create, manage, and display video advertisements and promotional banners/posters on the Golden Mais platform.

## Features

### 1. **Video Advertisements**
- Upload video files (MP4, WebM, OGV formats)
- Link to external video URLs (YouTube, Vimeo, etc.)
- Automatic video player with controls
- Support for both local and external video sources

### 2. **Banner/Poster Advertisements**
- Upload high-quality banner images
- Recommended dimensions: 1200x400px
- Display across the website
- Easy image management

### 3. **Advertisement Management**
- Create, read, update, and delete advertisements
- Set advertisement status (Draft, Active, Inactive, Archived)
- Control display order
- Schedule advertisements with start and end dates
- Track engagement metrics (views and clicks)

### 4. **Filtering & Organization**
- Filter by advertisement type (Video/Banner)
- Filter by status
- Pagination for easy browsing
- Organized list view with key information

## Accessing the Feature

### Admin Dashboard Navigation
1. Log in to the admin panel at `/admin-login/`
2. Navigate to **Advertisements** in the sidebar
3. You'll see the advertisements management page

### Quick Links
- **View All Advertisements**: `/admin-advertisements/`
- **Add New Advertisement**: `/admin-advertisement-add/`
- **Edit Advertisement**: `/admin-advertisement-edit/<id>/`
- **View Details**: `/admin-advertisement-view/<id>/`
- **Delete Advertisement**: `/admin-advertisement-delete/<id>/`

## How to Use

### Creating a Video Advertisement

1. Click **+ Add Advertisement** button
2. Fill in the following details:
   - **Title**: Name of the advertisement (required)
   - **Description**: Optional description
   - **Advertisement Type**: Select "Video Advertisement"
   - **Video File**: Upload a video file OR
   - **Video URL**: Provide a YouTube/Vimeo URL
   - **Status**: Choose from Draft, Active, Inactive, or Archived
   - **Display Order**: Lower numbers appear first (default: 0)
   - **Start Date**: Optional - when to start showing
   - **End Date**: Optional - when to stop showing

3. Click **Create Advertisement**

### Creating a Banner Advertisement

1. Click **+ Add Advertisement** button
2. Fill in the following details:
   - **Title**: Name of the banner (required)
   - **Description**: Optional description
   - **Advertisement Type**: Select "Banner/Poster"
   - **Banner Image**: Upload an image file (required)
   - **Status**: Choose from Draft, Active, Inactive, or Archived
   - **Display Order**: Lower numbers appear first (default: 0)
   - **Start Date**: Optional - when to start showing
   - **End Date**: Optional - when to stop showing

3. Click **Create Advertisement**

### Editing an Advertisement

1. Go to **Advertisements** page
2. Click **Edit** next to the advertisement you want to modify
3. Update the fields as needed
4. Click **Update Advertisement**

### Viewing Advertisement Details

1. Go to **Advertisements** page
2. Click **View** to see full details
3. On the details page, you can:
   - Preview the media (video or image)
   - View engagement metrics (views and clicks)
   - Change the status using the dropdown
   - Edit or delete the advertisement

### Deleting an Advertisement

1. Go to **Advertisements** page
2. Click **Delete** next to the advertisement
3. Review the confirmation page
4. Click **Yes, Delete Advertisement** to confirm

### Filtering Advertisements

1. Go to **Advertisements** page
2. Use the filter dropdowns:
   - **Type**: Filter by Video or Banner
   - **Status**: Filter by Draft, Active, Inactive, or Archived
3. Click **Filter** to apply
4. Click **Reset** to clear filters

## Advertisement Status Explained

| Status | Description |
|--------|-------------|
| **Draft** | Advertisement is saved but not visible to users |
| **Active** | Advertisement is visible to users (if within date range) |
| **Inactive** | Advertisement is temporarily hidden but not deleted |
| **Archived** | Advertisement is archived for historical records |

## Display Order

- Lower numbers are displayed first
- Default value is 0
- Advertisements with the same order are sorted by creation date (newest first)
- Example: Order 0 appears before Order 1, which appears before Order 2

## Scheduling Advertisements

### Using Start and End Dates

- **Start Date**: Advertisement becomes active on this date/time
- **End Date**: Advertisement becomes inactive after this date/time
- Both fields are optional
- If no dates are set, the advertisement displays based on status alone

### Example Scenarios

1. **Limited Time Promotion**
   - Status: Active
   - Start Date: Jan 1, 2024 at 00:00
   - End Date: Jan 31, 2024 at 23:59
   - Result: Shows only during January 2024

2. **Upcoming Campaign**
   - Status: Active
   - Start Date: Feb 1, 2024 at 00:00
   - End Date: (empty)
   - Result: Shows from Feb 1 onwards

3. **Past Campaign**
   - Status: Active
   - Start Date: (empty)
   - End Date: Dec 31, 2023 at 23:59
   - Result: Won't show (date has passed)

## Engagement Tracking

Each advertisement tracks:
- **Views**: Number of times the advertisement was displayed
- **Clicks**: Number of times users clicked on the advertisement

These metrics are displayed on the advertisement details page and help you measure campaign effectiveness.

## File Upload Guidelines

### Video Files
- **Supported Formats**: MP4, WebM, OGV
- **Maximum Size**: 500MB recommended
- **Recommended Resolution**: 1920x1080 (Full HD)
- **Aspect Ratio**: 16:9 preferred

### Banner Images
- **Supported Formats**: JPG, PNG, GIF, WebP
- **Recommended Size**: 1200x400px
- **Maximum Size**: 5MB recommended
- **Aspect Ratio**: 3:1 preferred

### Video URLs
- **Supported Platforms**: YouTube, Vimeo, and other standard video hosting
- **Format**: Full URL (e.g., https://www.youtube.com/watch?v=...)

## Best Practices

1. **Use Descriptive Titles**: Make titles clear and descriptive
2. **Optimize Images**: Compress images before uploading for faster loading
3. **Test Videos**: Test video playback before publishing
4. **Schedule Wisely**: Use start/end dates for time-sensitive promotions
5. **Monitor Engagement**: Check views and clicks to measure success
6. **Keep It Fresh**: Regularly update advertisements to maintain user interest
7. **Use Display Order**: Organize advertisements by importance
8. **Archive Old Ads**: Archive instead of deleting for record-keeping

## Troubleshooting

### Video Won't Play
- Check if the video format is supported (MP4, WebM, OGV)
- Verify the video file is not corrupted
- Try uploading a different video file
- If using URL, verify the link is correct and accessible

### Image Not Displaying
- Ensure the image format is supported
- Check if the image file is not corrupted
- Verify the file size is within limits
- Try uploading a different image

### Advertisement Not Showing
- Check if status is set to "Active"
- Verify the current date is within the start/end date range
- Ensure the advertisement is not archived
- Check if there are any JavaScript errors in the browser console

### Can't Upload File
- Check file size (max 500MB for videos, 5MB for images)
- Verify file format is supported
- Ensure you have sufficient storage space
- Try a different file

## Database Schema

The Advertisement model includes the following fields:

```python
- id: Auto-generated primary key
- title: CharField (max 200 characters)
- description: TextField (optional)
- ad_type: CharField (video or banner)
- video_file: FileField (optional)
- video_url: URLField (optional)
- image: ImageField (optional)
- status: CharField (draft, active, inactive, archived)
- display_order: PositiveIntegerField (default: 0)
- start_date: DateTimeField (optional)
- end_date: DateTimeField (optional)
- views: PositiveIntegerField (default: 0)
- clicks: PositiveIntegerField (default: 0)
- created_by: ForeignKey to User
- created_at: DateTimeField (auto-set)
- updated_at: DateTimeField (auto-update)
```

## API Endpoints (For Developers)

### Admin Routes
- `GET /admin-advertisements/` - List all advertisements
- `GET /admin-advertisement-add/` - Show add form
- `POST /admin-advertisement-add/` - Create advertisement
- `GET /admin-advertisement-edit/<id>/` - Show edit form
- `POST /admin-advertisement-edit/<id>/` - Update advertisement
- `GET /admin-advertisement-view/<id>/` - View details
- `GET /admin-advertisement-delete/<id>/` - Show delete confirmation
- `POST /admin-advertisement-delete/<id>/` - Delete advertisement
- `POST /admin-advertisement-toggle-status/<id>/` - Change status

## Security Notes

- Only admin users can access advertisement management
- All file uploads are validated
- File types are restricted to prevent security issues
- User input is sanitized to prevent XSS attacks
- CSRF protection is enabled on all forms

## Future Enhancements

Potential features for future versions:
- A/B testing for advertisements
- Advanced analytics dashboard
- Bulk operations (edit multiple ads at once)
- Advertisement templates
- Geolocation-based targeting
- Device-specific advertisements
- Advertisement rotation algorithms
- Performance metrics and ROI tracking

## Support

For issues or questions about the Advertisement Management feature, please contact the development team or refer to the main project documentation.

---

**Last Updated**: November 2024
**Feature Version**: 1.0
