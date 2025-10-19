# 🚀 Quick AWS Location Service Setup

## Current Issue
Your AWS user `BedrockAPIKey-a25j` needs Location Service permissions.

## 🔧 Step-by-Step Fix

### 1. Add Location Service Permissions
**Go to**: https://console.aws.amazon.com/iam/

1. **Click "Users"** in the left sidebar
2. **Find your user**: `BedrockAPIKey-a25j`
3. **Click on the username**
4. **Click "Add permissions"** button
5. **Select "Attach policies directly"**
6. **Search for**: `AmazonLocationServiceFullAccess`
7. **Check the box** next to it
8. **Click "Next"** → **"Add permissions"**

### 2. Create Place Index
**Go to**: https://console.aws.amazon.com/location/

1. **Click "Create place index"**
2. **Index name**: `HackathonPlaceIndex`
3. **Data source**: `Here`
4. **Pricing plan**: `RequestBasedUsage`
5. **Click "Create place index"**

### 3. Test Setup
Run this command:
```bash
python3 setup_location_service.py
```

## 🎯 Expected Result
You should see:
```
✅ Place Index created successfully!
📋 Index Name: HackathonPlaceIndex
🔍 Testing search functionality...
✅ Found 3 nearby places:
  1. Times Square
     Address: New York, NY
     Distance: 50m
```

## 🆘 If You Can't Add Permissions
If you can't modify IAM permissions, we can use alternative location services:
- Google Places API
- Foursquare API
- OpenStreetMap

Let me know if you need help with any of these steps!
