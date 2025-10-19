"""
Google Places API Location Service
Alternative to AWS Location Service for local business discovery
"""

import requests
import json
from typing import List, Dict, Optional
import os

class GoogleLocationService:
    """Google Places API integration for local business discovery"""
    
    def __init__(self):
        """Initialize Google Places API client"""
        self.api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        
    async def search_nearby_businesses(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int = 5000,  # 5km radius
        business_type: str = None,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for nearby businesses using Google Places API
        
        Args:
            latitude: User's latitude
            longitude: User's longitude  
            radius: Search radius in meters
            business_type: Type of business to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of business information dictionaries
        """
        if not self.api_key:
            print("⚠️ Google Places API key not found")
            return []
            
        try:
            # Prepare search parameters
            params = {
                'location': f"{latitude},{longitude}",
                'radius': radius,
                'key': self.api_key,
                'type': business_type or 'establishment'
            }
            
            # Perform the search
            response = requests.get(f"{self.base_url}/nearbysearch/json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
                return []
            
            # Extract and format business information
            businesses = []
            for place in data.get('results', [])[:max_results]:
                business_info = {
                    'name': place.get('name', 'Unknown'),
                    'address': place.get('vicinity', ''),
                    'phone': '',  # Will be filled by place details
                    'website': '',  # Will be filled by place details
                    'categories': [cat for cat in place.get('types', [])],
                    'latitude': place.get('geometry', {}).get('location', {}).get('lat'),
                    'longitude': place.get('geometry', {}).get('location', {}).get('lng'),
                    'distance': place.get('distance', 0),
                    'rating': place.get('rating', 0),
                    'place_id': place.get('place_id', '')
                }
                
                # Get additional details
                if business_info['place_id']:
                    details = await self._get_place_details(business_info['place_id'])
                    business_info.update(details)
                
                businesses.append(business_info)
            
            return businesses
            
        except Exception as e:
            print(f"Error searching nearby businesses: {e}")
            return []
    
    async def _get_place_details(self, place_id: str) -> Dict:
        """Get detailed information about a place"""
        try:
            params = {
                'place_id': place_id,
                'fields': 'formatted_phone_number,website,opening_hours',
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/details/json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK':
                result = data.get('result', {})
                return {
                    'phone': result.get('formatted_phone_number', ''),
                    'website': result.get('website', '')
                }
            
            return {}
            
        except Exception as e:
            print(f"Error getting place details: {e}")
            return {}
    
    async def search_businesses_by_text(
        self, 
        search_text: str, 
        latitude: float, 
        longitude: float,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for businesses by text query using Google Places API
        
        Args:
            search_text: Text to search for (e.g., "coffee shops", "bookstores")
            latitude: User's latitude
            longitude: User's longitude
            max_results: Maximum number of results to return
            
        Returns:
            List of business information dictionaries
        """
        if not self.api_key:
            print("⚠️ Google Places API key not found")
            return []
            
        try:
            # Prepare search parameters
            params = {
                'query': search_text,
                'location': f"{latitude},{longitude}",
                'radius': 5000,
                'key': self.api_key
            }
            
            # Perform the search
            response = requests.get(f"{self.base_url}/textsearch/json", params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                print(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
                return []
            
            # Extract and format business information
            businesses = []
            for place in data.get('results', [])[:max_results]:
                business_info = {
                    'name': place.get('name', 'Unknown'),
                    'address': place.get('formatted_address', ''),
                    'phone': '',
                    'website': '',
                    'categories': [cat for cat in place.get('types', [])],
                    'latitude': place.get('geometry', {}).get('location', {}).get('lat'),
                    'longitude': place.get('geometry', {}).get('location', {}).get('lng'),
                    'distance': 0,  # Text search doesn't provide distance
                    'rating': place.get('rating', 0),
                    'place_id': place.get('place_id', '')
                }
                
                # Get additional details
                if business_info['place_id']:
                    details = await self._get_place_details(business_info['place_id'])
                    business_info.update(details)
                
                businesses.append(business_info)
            
            return businesses
            
        except Exception as e:
            print(f"Error searching businesses by text: {e}")
            return []
    
    async def check_google_places_connection(self) -> bool:
        """Check if Google Places API is accessible"""
        if not self.api_key:
            return False
            
        try:
            # Test with a simple search
            params = {
                'query': 'test',
                'key': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/textsearch/json", params=params)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Google Places API connection failed: {e}")
            return False
