# Advertisement Management Feature - Testing Checklist

## Pre-Testing Setup

- [ ] Server is running (`python manage.py runserver`)
- [ ] Database migrations applied (`python manage.py migrate`)
- [ ] Admin account exists and logged in
- [ ] Media directory exists and is writable
- [ ] Static files collected (if in production)

---

## Admin Interface Testing

### Access & Navigation
- [ ] Can access `/admin-login/` page
- [ ] Can log in with admin credentials
- [ ] Admin dashboard loads successfully
- [ ] "Advertisements" appears in sidebar
- [ ] Can click "Advertisements" link
- [ ] Advertisements list page loads

### List View (`/admin-advertisements/`)
- [ ] Page displays correctly
- [ ] "Add Advertisement" button visible
- [ ] Filter dropdown for type works
- [ ] Filter dropdown for status works
- [ ] Filter button applies filters
- [ ] Reset button clears filters
- [ ] Pagination works (if more than 10 items)
- [ ] View, Edit, Delete buttons visible
- [ ] No advertisements message shows when empty

### Create Advertisement

#### Video Advertisement
- [ ] Click "+ Add Advertisement"
- [ ] Form displays correctly
- [ ] Title field is required
- [ ] Description field is optional
- [ ] Ad type dropdown shows "Video Advertisement"
- [ ] Video file upload field appears when type selected
- [ ] Video URL field appears when type selected
- [ ] Status dropdown shows all options
- [ ] Display order field accepts numbers
- [ ] Start date field accepts datetime
- [ ] End date field accepts datetime
- [ ] Can upload video file (MP4)
- [ ] Can enter video URL
- [ ] Form validation works (requires video file OR URL)
- [ ] Can submit form
- [ ] Success message appears
- [ ] Redirects to advertisements list
- [ ] New advertisement appears in list

#### Banner Advertisement
- [ ] Click "+ Add Advertisement"
- [ ] Select "Banner/Poster" type
- [ ] Image upload field appears
- [ ] Video fields disappear
- [ ] Can upload image file
- [ ] Form validation requires image
- [ ] Can submit form
- [ ] Success message appears
- [ ] New advertisement appears in list

### Edit Advertisement
- [ ] Click "Edit" on an advertisement
- [ ] Form pre-fills with existing data
- [ ] Can modify title
- [ ] Can modify description
- [ ] Can change status
- [ ] Can modify display order
- [ ] Can change dates
- [ ] Can upload new image/video
- [ ] Can submit changes
- [ ] Success message appears
- [ ] Changes are saved

### View Details
- [ ] Click "View" on an advertisement
- [ ] Details page loads
- [ ] Title displays correctly
- [ ] Media preview shows (image or video player)
- [ ] Description displays
- [ ] Status badge shows correct status
- [ ] Engagement metrics display (views, clicks)
- [ ] Created by information shows
- [ ] Created date shows
- [ ] Updated date shows
- [ ] Status dropdown works
- [ ] Can change status from details page
- [ ] Edit button works
- [ ] Back button works

### Delete Advertisement
- [ ] Click "Delete" on an advertisement
- [ ] Confirmation page loads
- [ ] Advertisement details shown
- [ ] Warning message displayed
- [ ] "Yes, Delete" button visible
- [ ] "Cancel" button visible
- [ ] Can confirm deletion
- [ ] Advertisement removed from list
- [ ] Success message appears
- [ ] Can cancel deletion

### Status Management
- [ ] Can change status from Draft to Active
- [ ] Can change status from Active to Inactive
- [ ] Can change status from Inactive to Archived
- [ ] Can change status in any direction
- [ ] Status changes are saved
- [ ] Success messages appear

### Filtering
- [ ] Filter by "Video Advertisement" type
- [ ] Filter by "Banner/Poster" type
- [ ] Filter by "Draft" status
- [ ] Filter by "Active" status
- [ ] Filter by "Inactive" status
- [ ] Filter by "Archived" status
- [ ] Combine type and status filters
- [ ] Reset filters clears all selections
- [ ] Pagination works with filters

---

## Frontend Testing

### Homepage (`/`)
- [ ] Page loads successfully
- [ ] Hero section displays
- [ ] Promotional advertisements section appears (if ads exist)
- [ ] Section title "🎯 Special Promotions" shows
- [ ] Advertisement cards display in grid
- [ ] Images display correctly
- [ ] Titles display correctly
- [ ] Descriptions display correctly
- [ ] Hover effects work (scale and shadow)
- [ ] Responsive on mobile (1 column)
- [ ] Responsive on tablet (2 columns)
- [ ] Responsive on desktop (3 columns)
- [ ] Featured products section still displays
- [ ] Combo deals section still displays

### Promotions Page (`/promotions/`)
- [ ] Page loads successfully
- [ ] Header section displays
- [ ] Video advertisements section shows (if videos exist)
- [ ] Banner advertisements section shows (if banners exist)
- [ ] Video player works for uploaded videos
- [ ] External video links work
- [ ] Engagement metrics display
- [ ] No advertisements message shows when empty
- [ ] Newsletter signup section displays
- [ ] Call-to-action buttons work
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop

### Navigation
- [ ] "🎯 Promotions" link appears in desktop menu
- [ ] "🎯 Promotions" link appears in mobile menu
- [ ] Link is between Products and Contact
- [ ] Link is active/highlighted when on promotions page
- [ ] Link navigates to `/promotions/`
- [ ] Can navigate back from promotions page

---

## Date Scheduling Testing

### Always Active Advertisement
- [ ] Create ad with Active status
- [ ] Leave Start Date empty
- [ ] Leave End Date empty
- [ ] Ad displays on homepage
- [ ] Ad displays on promotions page

### Limited Time Promotion
- [ ] Create ad with Active status
- [ ] Set Start Date to today
- [ ] Set End Date to tomorrow
- [ ] Ad displays on homepage
- [ ] Ad displays on promotions page

### Upcoming Campaign
- [ ] Create ad with Active status
- [ ] Set Start Date to tomorrow
- [ ] Leave End Date empty
- [ ] Ad does NOT display yet
- [ ] Change Start Date to today
- [ ] Ad now displays

### Expired Campaign
- [ ] Create ad with Active status
- [ ] Set End Date to yesterday
- [ ] Ad does NOT display
- [ ] Change End Date to tomorrow
- [ ] Ad now displays

---

## Status Display Testing

### Draft Status
- [ ] Create ad with Draft status
- [ ] Ad does NOT appear on homepage
- [ ] Ad does NOT appear on promotions page
- [ ] Ad appears in admin list
- [ ] Status badge shows "Draft"

### Active Status
- [ ] Create ad with Active status
- [ ] Ad appears on homepage (if banner)
- [ ] Ad appears on promotions page
- [ ] Status badge shows "Active"

### Inactive Status
- [ ] Create ad with Active status
- [ ] Change to Inactive status
- [ ] Ad disappears from homepage
- [ ] Ad disappears from promotions page
- [ ] Ad still appears in admin list
- [ ] Status badge shows "Inactive"

### Archived Status
- [ ] Create ad with Active status
- [ ] Change to Archived status
- [ ] Ad disappears from homepage
- [ ] Ad disappears from promotions page
- [ ] Ad still appears in admin list
- [ ] Status badge shows "Archived"

---

## File Upload Testing

### Video File Upload
- [ ] Upload MP4 file
- [ ] Upload WebM file
- [ ] Upload OGV file
- [ ] Video plays in player
- [ ] Cannot upload unsupported format
- [ ] Error message shows for invalid format
- [ ] File size limit enforced

### Image Upload
- [ ] Upload JPG file
- [ ] Upload PNG file
- [ ] Upload GIF file
- [ ] Upload WebP file
- [ ] Image displays correctly
- [ ] Cannot upload unsupported format
- [ ] Error message shows for invalid format
- [ ] File size limit enforced

### Video URL
- [ ] Enter YouTube URL
- [ ] Enter Vimeo URL
- [ ] Video link works
- [ ] Invalid URL shows error

---

## API Testing

### Carousel API (`/api/advertisements/carousel/`)
- [ ] Endpoint returns JSON
- [ ] Returns only banner advertisements
- [ ] Returns only active advertisements
- [ ] Respects date range filtering
- [ ] Returns correct fields (id, title, image_url, description)
- [ ] Returns empty array when no ads

### Videos API (`/api/advertisements/videos/`)
- [ ] Endpoint returns JSON
- [ ] Returns only video advertisements
- [ ] Returns only active advertisements
- [ ] Respects date range filtering
- [ ] Returns correct fields (id, title, video_url, video_file, description)
- [ ] Returns empty array when no ads

---

## Responsive Design Testing

### Mobile (375px width)
- [ ] Homepage ads: 1 column
- [ ] Promotions page: 1 column
- [ ] Navigation menu works
- [ ] All buttons clickable
- [ ] Images scale properly
- [ ] Text readable

### Tablet (768px width)
- [ ] Homepage ads: 2 columns
- [ ] Promotions page: 2 columns
- [ ] Navigation menu works
- [ ] All buttons clickable
- [ ] Images scale properly
- [ ] Text readable

### Desktop (1024px+ width)
- [ ] Homepage ads: 3 columns
- [ ] Promotions page: 2-3 columns
- [ ] Navigation menu works
- [ ] All buttons clickable
- [ ] Images scale properly
- [ ] Text readable

---

## Performance Testing

### Load Time
- [ ] Homepage loads in < 3 seconds
- [ ] Promotions page loads in < 3 seconds
- [ ] Admin list loads in < 2 seconds
- [ ] API endpoints respond in < 1 second

### Database
- [ ] Queries are efficient
- [ ] No N+1 query problems
- [ ] Pagination works smoothly
- [ ] Filtering is fast

### File Handling
- [ ] Large images upload successfully
- [ ] Large videos upload successfully
- [ ] Files serve quickly
- [ ] No broken links

---

## Security Testing

### Access Control
- [ ] Non-admin users cannot access admin pages
- [ ] Non-admin users cannot create advertisements
- [ ] Non-admin users cannot edit advertisements
- [ ] Non-admin users cannot delete advertisements
- [ ] Customers can view advertisements

### Form Validation
- [ ] Required fields enforced
- [ ] File type validation works
- [ ] File size validation works
- [ ] Date validation works
- [ ] Input sanitization works

### CSRF Protection
- [ ] Forms include CSRF token
- [ ] CSRF validation works
- [ ] Invalid tokens rejected

---

## Error Handling Testing

### Missing Files
- [ ] Missing image shows placeholder
- [ ] Missing video shows error message
- [ ] Missing URL shows error message

### Invalid Data
- [ ] Invalid date format shows error
- [ ] Invalid file type shows error
- [ ] Missing required fields shows error
- [ ] Duplicate titles allowed (not unique)

### Database Errors
- [ ] Handles database connection errors
- [ ] Handles query errors gracefully
- [ ] Shows user-friendly error messages

---

## Browser Compatibility Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## User Experience Testing

### Admin Experience
- [ ] Intuitive interface
- [ ] Clear labels and instructions
- [ ] Helpful error messages
- [ ] Smooth workflows
- [ ] Fast operations

### Customer Experience
- [ ] Easy to find promotions
- [ ] Clear advertisement display
- [ ] Smooth video playback
- [ ] Responsive design
- [ ] Fast loading

---

## Data Integrity Testing

### Create Operations
- [ ] Data saved correctly
- [ ] All fields populated
- [ ] Timestamps set correctly
- [ ] Creator recorded

### Update Operations
- [ ] Changes saved correctly
- [ ] Old data not lost
- [ ] Timestamps updated
- [ ] History preserved

### Delete Operations
- [ ] Data removed from database
- [ ] Files deleted from storage
- [ ] No orphaned records
- [ ] Referential integrity maintained

---

## Regression Testing

- [ ] Homepage still works
- [ ] Products page still works
- [ ] Shopping cart still works
- [ ] Checkout still works
- [ ] Admin dashboard still works
- [ ] Other admin features still work
- [ ] Customer account features still work

---

## Final Sign-Off

- [ ] All tests passed
- [ ] No critical bugs found
- [ ] No performance issues
- [ ] Documentation complete
- [ ] Ready for production deployment

**Tested By**: ___________________
**Date**: ___________________
**Status**: ✅ APPROVED / ❌ NEEDS FIXES

---

## Notes & Issues Found

```
[Space for documenting any issues found during testing]
```

---

**Last Updated**: November 27, 2025
**Version**: 1.0
