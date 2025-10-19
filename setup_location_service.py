#!/usr/bin/env python3
"""
AWS Location Service Setup Script for BridgeTales AI
This script helps you set up the AWS Location Service for real business data.
"""

import boto3
import json
from config import Config

def create_place_index():
    """Create a Place Index in AWS Location Service"""
    try:
        # Initialize Location Service client
        client = boto3.client(
            'location',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        # Place Index configuration
        place_index_name = "HackathonPlaceIndex"
        
        print(f"🚀 Creating Place Index: {place_index_name}")
        print(f"📍 Region: {Config.AWS_REGION}")
        
        # Create the Place Index
        response = client.create_place_index(
            IndexName=place_index_name,
            DataSource="Here",  # You can also use "Esri"
            DataSourceConfiguration={
                'IntendedUse': 'SingleUse'  # or 'Storage' for multiple uses
            },
            Description="BridgeTales AI Location Service for local business discovery",
            PricingPlan="RequestBasedUsage"  # or "MobileAssetTracking" for mobile apps
        )
        
        print(f"✅ Place Index created successfully!")
        print(f"📋 Index Name: {response['IndexName']}")
        print(f"🔗 Index ARN: {response['IndexArn']}")
        
        return True
        
    except client.exceptions.ConflictException:
        print(f"ℹ️  Place Index '{place_index_name}' already exists!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Place Index: {e}")
        return False

def test_location_service():
    """Test the Location Service connection"""
    try:
        client = boto3.client(
            'location',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        # List existing place indexes
        response = client.list_place_indexes()
        indexes = response.get('IndexEntries', [])
        
        print(f"📋 Found {len(indexes)} Place Index(es):")
        for index in indexes:
            print(f"  - {index['IndexName']} (Created: {index['CreateTime']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Location Service: {e}")
        return False

def search_nearby_test():
    """Test searching for nearby places"""
    try:
        client = boto3.client(
            'location',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        # Test with a known location (Times Square, NYC)
        test_lat = 40.7589
        test_lng = -73.9851
        
        print(f"🔍 Testing search near Times Square, NYC...")
        
        response = client.search_place_index_for_position(
            IndexName="HackathonPlaceIndex",
            Position=[test_lng, test_lat],  # Note: AWS uses [longitude, latitude]
            MaxResults=3
        )
        
        results = response.get('Results', [])
        print(f"✅ Found {len(results)} nearby places:")
        
        for i, result in enumerate(results, 1):
            place = result.get('Place', {})
            print(f"  {i}. {place.get('Label', 'Unknown')}")
            print(f"     Address: {place.get('Address', 'N/A')}")
            print(f"     Distance: {result.get('Distance', 'N/A')}m")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing search: {e}")
        return False

def main():
    """Main setup function"""
    print("🌍 AWS Location Service Setup for BridgeTales AI")
    print("=" * 50)
    
    # Validate AWS credentials
    if not Config.AWS_ACCESS_KEY_ID or not Config.AWS_SECRET_ACCESS_KEY:
        print("❌ AWS credentials not found!")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        return False
    
    print(f"✅ AWS credentials found")
    print(f"📍 Region: {Config.AWS_REGION}")
    
    # Test connection
    print("\n🔗 Testing Location Service connection...")
    if not test_location_service():
        return False
    
    # Create Place Index
    print("\n🏗️  Creating Place Index...")
    if not create_place_index():
        return False
    
    # Test search functionality
    print("\n🔍 Testing search functionality...")
    if not search_nearby_test():
        print("⚠️  Search test failed, but Place Index was created")
        print("You may need to wait a few minutes for the index to be ready")
    
    print("\n🎉 Setup complete!")
    print("Your BridgeTales AI app can now use real location data!")
    
    return True

if __name__ == "__main__":
    main()
