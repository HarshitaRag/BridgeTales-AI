import boto3
import json
from typing import List, Dict, Optional
from config import Config
from .google_location_service import GoogleLocationService

PLACE_INDEX_NAME = "HackathonPlaceIndex"
class LocationService:
    """AWS Location Service integration for local business discovery"""
    
    def __init__(self):
        """Initialize AWS Location Service client"""
        self.client = boto3.client(
            'location',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        # Place index name - you'll need to create this in AWS Console
        self.place_index_name = PLACE_INDEX_NAME
        
        # Initialize Google Places as fallback
        self.google_service = GoogleLocationService()
        self.aws_available = None  # Will be set on first check
    
    async def search_nearby_businesses(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int = 5000,  # 5km radius
        categories: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for nearby businesses using the best available service
        
        Args:
            latitude: User's latitude
            longitude: User's longitude  
            radius: Search radius in meters (default 5km)
            categories: List of business categories to filter by
            max_results: Maximum number of results to return
            
        Returns:
            List of business information dictionaries
        """
        service = await self._get_available_service()
        
        if service == "aws":
            return await self._search_aws_nearby(latitude, longitude, radius, categories, max_results)
        elif service == "google":
            return await self.google_service.search_nearby_businesses(latitude, longitude, radius, None, max_results)
        else:
            return await self._get_demo_businesses()
    
    async def _search_aws_nearby(
        self, 
        latitude: float, 
        longitude: float, 
        radius: int = 5000,
        categories: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[Dict]:
        """Search using AWS Location Service"""
        try:
            # Prepare search parameters
            search_params = {
                'IndexName': self.place_index_name,
                'Position': [longitude, latitude],  # Note: AWS uses [lng, lat] format
                'MaxResults': max_results
            }
            
            # Add category filter if provided
            if categories:
                search_params['FilterCategories'] = categories
            
            # Perform the search
            response = self.client.search_place_index_for_position(**search_params)
            
            # Extract and format business information
            businesses = []
            for result in response.get('Results', []):
                place = result.get('Place', {})
                business_info = {
                    'name': place.get('Label', 'Unknown'),
                    'address': place.get('Address', ''),
                    'phone': place.get('PhoneNumber', ''),
                    'website': place.get('Website', ''),
                    'categories': place.get('Categories', []),
                    'latitude': place.get('Geometry', {}).get('Point', [None, None])[1],
                    'longitude': place.get('Geometry', {}).get('Point', [None, None])[0],
                    'distance': result.get('Distance', 0)
                }
                businesses.append(business_info)
            
            return businesses
            
        except Exception as e:
            print(f"Error searching nearby businesses with AWS: {e}")
            return []
    
    async def search_businesses_by_text(
        self, 
        search_text: str, 
        latitude: float, 
        longitude: float,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for businesses by text query using the best available service
        
        Args:
            search_text: Text to search for (e.g., "coffee shops", "bookstores")
            latitude: User's latitude
            longitude: User's longitude
            max_results: Maximum number of results to return
            
        Returns:
            List of business information dictionaries
        """
        service = await self._get_available_service()
        
        if service == "aws":
            return await self._search_aws_text(search_text, latitude, longitude, max_results)
        elif service == "google":
            return await self.google_service.search_businesses_by_text(search_text, latitude, longitude, max_results)
        else:
            return await self._get_demo_businesses()
    
    async def _search_aws_text(
        self, 
        search_text: str, 
        latitude: float, 
        longitude: float,
        max_results: int = 10
    ) -> List[Dict]:
        """Search using AWS Location Service text search - BUSINESSES ONLY"""
        try:
            # Prepare search parameters - ONLY cafes and parks
            search_params = {
                'IndexName': self.place_index_name,
                'Text': search_text,
                'BiasPosition': [longitude, latitude],  # Note: AWS uses [lng, lat] format
                'MaxResults': max_results * 5,  # Get many more results to filter for local only
                'FilterCategories': [
                    'Cafe',
                    'CoffeeShop',
                    'Park',
                    'Recreation',
                    'Garden'
                ]
            }
            
            # Perform the search
            response = self.client.search_place_index_for_text(**search_params)
            
            # Extract and format business information - LOCAL BUSINESSES ONLY
            businesses = []
            
            # List of chain stores to exclude (only want local businesses)
            chain_exclusions = [
                'starbucks', 'mcdonalds', 'burger king', 'wendys', 'subway', 'taco bell',
                'pizza hut', 'dominos', 'papa johns', 'kfc', 'popeyes', 'chipotle',
                'panera', 'dunkin', 'tim hortons', 'costa', 'peets', 'caribou',
                'target', 'walmart', 'costco', 'cvs', 'walgreens', 'rite aid',
                'whole foods', '7-eleven', 'circle k', 'shell', 'chevron', 'bp',
                'applebees', 'olive garden', 'chilis', 'red lobster', 'outback',
                'ihop', 'dennys', 'cracker barrel', 'buffalo wild wings'
            ]
            
            for result in response.get('Results', []):
                place = result.get('Place', {})
                categories = place.get('Categories', [])
                label = place.get('Label', 'Unknown')
                name = label.split(',')[0].lower()  # Get business name
                
                # Skip residential addresses and street addresses
                if any(skip in label.lower() for skip in ['street', 'avenue', 'road', 'lane', 'drive', 'way']):
                    if not categories:  # Only skip if no business categories
                        continue
                
                # Skip chain stores - ONLY LOCAL BUSINESSES
                if any(chain in name for chain in chain_exclusions):
                    continue
                
                # Only include cafes and parks
                relevant_categories = ['cafe', 'coffee', 'park', 'garden', 'recreation']
                has_relevant_category = any(
                    any(rel_cat in cat.lower() for rel_cat in relevant_categories)
                    for cat in categories
                )
                
                # Only include if it has cafe/park categories
                if has_relevant_category and categories and len(categories) > 0:
                    business_info = {
                        'name': label.split(',')[0],  # Just the business name, not full address
                        'address': ', '.join(label.split(',')[1:]).strip() if ',' in label else place.get('Address', ''),
                        'phone': place.get('PhoneNumber', ''),
                        'website': place.get('Website', ''),
                        'categories': categories,
                        'latitude': place.get('Geometry', {}).get('Point', [None, None])[1],
                        'longitude': place.get('Geometry', {}).get('Point', [None, None])[0],
                        'distance': result.get('Distance', 0)
                    }
                    businesses.append(business_info)
                    
                    if len(businesses) >= max_results:
                        break
            
            return businesses[:max_results]
            
        except Exception as e:
            print(f"Error searching businesses by text with AWS: {e}")
            return []
    
    async def find_story_related_businesses(
        self, 
        story_context: str, 
        latitude: float, 
        longitude: float,
        max_results: int = 5
    ) -> List[Dict]:
        """
        Find businesses related to story context using intelligent search
        
        Args:
            story_context: The story content to analyze
            latitude: User's latitude
            longitude: User's longitude
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant business information dictionaries
        """
        try:
            # Extract keywords and themes from story context
            search_terms = self._extract_search_terms(story_context)
            
            all_businesses = []
            
            # Search for each relevant term
            for term in search_terms[:3]:  # Limit to top 3 terms
                businesses = await self.search_businesses_by_text(
                    term, latitude, longitude, max_results=3
                )
                all_businesses.extend(businesses)
            
            # Remove duplicates and sort by relevance
            unique_businesses = self._deduplicate_businesses(all_businesses)
            return unique_businesses[:max_results]
            
        except Exception as e:
            print(f"Error finding story-related businesses: {e}")
            return await self._get_demo_businesses()
    
    def _extract_search_terms(self, story_context: str) -> List[str]:
        """
        Extract relevant search terms from story context
        This is a simple implementation - you could enhance with NLP
        """
        # Simple keyword extraction based on common story themes
        story_lower = story_context.lower()
        
        # Map story themes to business categories
        theme_mappings = {
            'coffee': ['coffee shop', 'cafe', 'coffee'],
            'book': ['bookstore', 'library', 'book shop'],
            'food': ['restaurant', 'food', 'dining'],
            'park': ['park', 'playground', 'outdoor'],
            'museum': ['museum', 'gallery', 'exhibition'],
            'shop': ['shop', 'store', 'retail'],
            'play': ['playground', 'park', 'recreation'],
            'learn': ['school', 'library', 'education'],
            'art': ['art gallery', 'museum', 'art studio'],
            'music': ['music store', 'concert hall', 'music venue']
        }
        
        search_terms = []
        for theme, terms in theme_mappings.items():
            if theme in story_lower:
                search_terms.extend(terms)
        
        # If no specific themes found, try general terms
        if not search_terms:
            search_terms = ['local business', 'shop', 'restaurant']
        
        return search_terms[:5]  # Return top 5 terms
    
    def _deduplicate_businesses(self, businesses: List[Dict]) -> List[Dict]:
        """Remove duplicate businesses based on name and address"""
        seen = set()
        unique_businesses = []
        
        for business in businesses:
            # Create a unique identifier
            identifier = f"{business.get('name', '')}_{business.get('address', '')}"
            if identifier not in seen:
                seen.add(identifier)
                unique_businesses.append(business)
        
        return unique_businesses
    
    async def _check_aws_availability(self) -> bool:
        """Check if AWS Location Service is available"""
        if self.aws_available is not None:
            return self.aws_available
            
        try:
            # Try to list place indexes (this is a lightweight operation)
            self.client.list_place_indexes()
            self.aws_available = True
            print("✅ AWS Location Service is available")
            return True
        except Exception as e:
            print(f"AWS Location Service not available: {e}")
            self.aws_available = False
            return False
    
    async def _get_available_service(self):
        """Get the best available location service"""
        if await self._check_aws_availability():
            return "aws"
        elif await self.google_service.check_google_places_connection():
            print("✅ Using Google Places API as fallback")
            return "google"
        else:
            print("⚠️ No location services available, using demo data")
            return "demo"
    
    async def _get_demo_businesses(self) -> List[Dict]:
        """Get demo businesses for testing"""
        return [
            {
                'name': "The Friendship Café",
                'address': "123 Main Street, Your City",
                'phone': "(555) 123-4567",
                'website': "https://example.com",
                'categories': ["Restaurant", "Coffee Shop"],
                'distance': 250
            },
            {
                'name': "Adventure Bookstore",
                'address': "456 Oak Avenue, Your City", 
                'phone': "(555) 987-6543",
                'website': "https://bookstore.com",
                'categories': ["Bookstore", "Education"],
                'distance': 500
            },
            {
                'name': "Kindness Community Center",
                'address': "789 Pine Street, Your City",
                'phone': "(555) 456-7890",
                'website': "https://community.org",
                'categories': ["Community Center", "Volunteer"],
                'distance': 800
            }
        ]
    
    async def check_location_service_connection(self) -> bool:
        """Check if any location service is accessible"""
        return await self._check_aws_availability() or await self.google_service.check_google_places_connection()
