#!/usr/bin/env python3
"""
Test Location Service Integration
This script tests the location service with different scenarios
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.location_service import LocationService

async def test_location_service():
    """Test the location service with different scenarios"""
    print("🧪 Testing Location Service Integration")
    print("=" * 50)
    
    # Initialize the service
    location_service = LocationService()
    
    # Test 1: Check service availability
    print("\n1️⃣ Testing service availability...")
    aws_available = await location_service._check_aws_availability()
    google_available = await location_service.google_service.check_google_places_connection()
    
    print(f"   AWS Location Service: {'✅ Available' if aws_available else '❌ Not available'}")
    print(f"   Google Places API: {'✅ Available' if google_available else '❌ Not available'}")
    
    # Test 2: Get available service
    print("\n2️⃣ Determining best service...")
    service = await location_service._get_available_service()
    print(f"   Selected service: {service.upper()}")
    
    # Test 3: Search for nearby businesses
    print("\n3️⃣ Testing business search...")
    test_lat = 40.7589  # Times Square, NYC
    test_lng = -73.9851
    
    businesses = await location_service.search_nearby_businesses(
        latitude=test_lat,
        longitude=test_lng,
        max_results=3
    )
    
    print(f"   Found {len(businesses)} businesses:")
    for i, business in enumerate(businesses, 1):
        print(f"   {i}. {business['name']}")
        print(f"      Address: {business['address']}")
        print(f"      Distance: {business.get('distance', 'N/A')}m")
    
    # Test 4: Story-related search
    print("\n4️⃣ Testing story-related search...")
    story_context = "A story about friendship and adventure in a magical forest"
    
    story_businesses = await location_service.find_story_related_businesses(
        story_context=story_context,
        latitude=test_lat,
        longitude=test_lng,
        max_results=3
    )
    
    print(f"   Found {len(story_businesses)} story-related businesses:")
    for i, business in enumerate(story_businesses, 1):
        print(f"   {i}. {business['name']}")
        print(f"      Categories: {', '.join(business.get('categories', []))}")
    
    print("\n🎉 Location Service test complete!")
    print("\n💡 To get real AWS data:")
    print("   1. Add Location Service permissions to your AWS user")
    print("   2. Create Place Index in AWS Console")
    print("   3. Run this test again")

if __name__ == "__main__":
    asyncio.run(test_location_service())
