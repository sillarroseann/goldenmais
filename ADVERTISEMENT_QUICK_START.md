# Advertisement Management - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Access the Feature
1. Log in to admin dashboard at `/admin-login/`
2. Look for **"Advertisements"** in the left sidebar
3. Click it to see all advertisements

### Step 2: Create Your First Advertisement

#### For Video Ads:
1. Click **"+ Add Advertisement"** button
2. Fill in:
   - **Title**: "Summer Corn Sale"
   - **Description**: "Check out our fresh summer corn collection"
   - **Type**: Select "Video Advertisement"
   - **Video**: Either upload a file OR paste a YouTube URL
   - **Status**: Select "Active"
3. Click **"Create Advertisement"**

#### For Banner Ads:
1. Click **"+ Add Advertisement"** button
2. Fill in:
   - **Title**: "Holiday Special"
   - **Description**: "Limited time offer"
   - **Type**: Select "Banner/Poster"
   - **Image**: Upload a banner image (1200x400px recommended)
   - **Status**: Select "Active"
3. Click **"Create Advertisement"**

### Step 3: Manage Your Ads
- **View**: Click "View" to see details and engagement metrics
- **Edit**: Click "Edit" to make changes
- **Delete**: Click "Delete" to remove
- **Filter**: Use dropdowns to filter by type or status

---

## 📋 Quick Reference

### Status Options
| Status | Meaning |
|--------|---------|
| 🟢 Active | Visible to users now |
| 🟡 Draft | Saved but hidden |
| ⚫ Inactive | Temporarily hidden |
| 📦 Archived | Historical record |

### File Requirements
| Type | Format | Size | Recommended |
|------|--------|------|-------------|
| Video | MP4, WebM, OGV | <500MB | 1920x1080 |
| Image | JPG, PNG, GIF | <5MB | 1200x400px |

### Display Order
- Lower numbers = shown first
- Example: Order 0 before Order 1 before Order 2

---

## 💡 Pro Tips

✅ **DO:**
- Use clear, descriptive titles
- Compress images before uploading
- Schedule ads for specific time periods
- Check engagement metrics regularly
- Archive old ads instead of deleting

❌ **DON'T:**
- Upload huge files (use compression)
- Leave ads in "Draft" status by accident
- Use poor quality images
- Forget to set an end date for limited offers

---

## 🔗 Quick Links

| Action | URL |
|--------|-----|
| View All Ads | `/admin-advertisements/` |
| Add New Ad | `/admin-advertisement-add/` |
| Edit Ad | `/admin-advertisement-edit/<id>/` |
| View Details | `/admin-advertisement-view/<id>/` |
| Delete Ad | `/admin-advertisement-delete/<id>/` |

---

## ⏰ Scheduling Examples

### Example 1: Flash Sale (1 Day)
- Status: Active
- Start: Jan 15, 2024 at 00:00
- End: Jan 15, 2024 at 23:59
- Result: Shows only on Jan 15

### Example 2: Seasonal Campaign (1 Month)
- Status: Active
- Start: Dec 1, 2023 at 00:00
- End: Dec 31, 2023 at 23:59
- Result: Shows throughout December

### Example 3: Ongoing Promotion
- Status: Active
- Start: (leave empty)
- End: (leave empty)
- Result: Shows indefinitely until status changed

---

## 🎯 Common Tasks

### Task: Change Ad Status
1. Go to Advertisements page
2. Click "View" on the ad
3. Use the dropdown to select new status
4. Click "Update Status"

### Task: Schedule an Ad
1. Click "Edit" on the ad
2. Set "Start Date" and/or "End Date"
3. Click "Update Advertisement"

### Task: Find Underperforming Ads
1. Go to Advertisements page
2. Click "View" on each ad
3. Check "Views" and "Clicks" metrics
4. Consider archiving low-performing ads

### Task: Reorder Ads
1. Click "Edit" on the ad
2. Change the "Display Order" number
3. Click "Update Advertisement"
4. Lower numbers appear first

---

## ❓ Troubleshooting

**Video won't play?**
- Check file format (MP4, WebM, OGV)
- Verify file isn't corrupted
- Try uploading again

**Image not showing?**
- Ensure format is supported (JPG, PNG, GIF)
- Check file size
- Try a different image

**Ad not visible?**
- Check status is "Active"
- Verify date range (if set)
- Check display order

**Can't upload file?**
- Check file size limits
- Verify file format
- Try a smaller file

---

## 📊 Understanding Metrics

- **Views**: How many times the ad was displayed
- **Clicks**: How many times users clicked on it
- **Click Rate**: Clicks ÷ Views = engagement quality

---

## 🎨 Design Tips

### For Videos
- Keep under 30 seconds for best engagement
- Use captions for accessibility
- Ensure good video quality
- Test on mobile devices

### For Banners
- Use high contrast colors
- Include a clear call-to-action
- Keep text minimal
- Use professional images

---

## 📞 Need Help?

- Check the full guide: `ADVERTISEMENT_FEATURE_GUIDE.md`
- Review implementation details: `ADVERTISEMENT_IMPLEMENTATION_SUMMARY.md`
- Contact the development team

---

**Last Updated**: November 2024
**Version**: 1.0
