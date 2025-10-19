# AWS Location Service Setup Guide

## 🚨 Current Issue
Your AWS user doesn't have Location Service permissions. Here's how to fix it:

## 🔧 Option 1: Add Location Service Permissions (Recommended)

### Step 1: Go to AWS IAM Console
1. Open [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Go to "Users" → Find your user (BedrockAPIKey-a25j)
3. Click "Add permissions" → "Attach policies directly"

### Step 2: Add Location Service Policy
Search for and attach this policy:
```
AmazonLocationServiceFullAccess
```

### Step 3: Create Place Index
1. Go to [AWS Location Service Console](https://console.aws.amazon.com/location/)
2. Click "Create place index"
3. Name: `HackathonPlaceIndex`
4. Data source: `Here` (recommended)
5. Pricing plan: `RequestBasedUsage`
6. Click "Create place index"

## 🔧 Option 2: Use Alternative Location Service

If you can't get Location Service permissions, we can use:
- Google Places API
- Foursquare API
- OpenStreetMap Nominatim

## 🧪 Test Your Setup

Once you have permissions, run:
```bash
python3 setup_location_service.py
```

## 📋 Required Permissions

Your AWS user needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
        "Action": [
            "geo:CreatePlaceIndex",
            "geo:ListPlaceIndexes",
            "geo:SearchPlaceIndexForPosition",
            "geo:SearchPlaceIndexForText"
        ],
        "Resource": "*"
        }
    ]
}
```

## 🎯 Next Steps

1. **Add Location Service permissions** to your AWS user
2. **Create the Place Index** in AWS Console
3. **Test the setup** with our script
4. **Enjoy real location data** in your app!

## 💡 Alternative: Keep Demo Data

If you prefer to keep the demo data for now, the app will work perfectly with the sample businesses we created!
