import os
import json
from datetime import datetime

try:
    from pinecone.grpc import PineconeGRPC as Pinecone
    from pinecone import ServerlessSpec
except ImportError:
    # Fallback for older versions
    from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key="pcsk_6vhZMA_4Rh1K18qztL13jHvvmd8vUw7B2ahbWzh8qc7r6RtnwGh7PJf4eRuZxZH3zczQTL")

# Index name
INDEX_NAME = "bridgetales-users"

def get_or_create_index():
    """Get or create Pinecone index"""
    try:
        # List existing indexes
        existing_indexes = pc.list_indexes()
        index_names = [idx.name for idx in existing_indexes]
        
        if INDEX_NAME not in index_names:
            # Create index if it doesn't exist
            pc.create_index(
                name=INDEX_NAME,
                dimension=384,  # Standard dimension for text embeddings
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        
        return pc.Index(INDEX_NAME)
    except Exception as e:
        print(f"Pinecone index error: {e}")
        return None

async def save_profile_to_pinecone(profile_data):
    """Save user profile to Pinecone"""
    try:
        index = get_or_create_index()
        if not index:
            return
        
        # Create a simple embedding (you can use actual embeddings later)
        user_id = f"user_{profile_data['name'].lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
        
        # Store profile with metadata
        vector = [0.1] * 384  # Placeholder vector
        
        index.upsert(
            vectors=[{
                "id": user_id,
                "values": vector,
                "metadata": {
                    "type": "profile",
                    "name": profile_data['name'],
                    "age": profile_data['age'],
                    "voice": profile_data['voice'],
                    "created_at": datetime.now().isoformat()
                }
            }]
        )
        
        print(f"✅ Profile saved to Pinecone: {user_id}")
    except Exception as e:
        print(f"❌ Error saving profile to Pinecone: {e}")

async def save_book_to_pinecone(book_data):
    """Save completed book to Pinecone"""
    try:
        index = get_or_create_index()
        if not index:
            return
        
        book_id = f"book_{book_data['id']}"
        
        # Create summary for embedding
        summary = f"Theme: {book_data['theme']}. Pages: {len(book_data['pages'])}. Completed by: {book_data['userName']}"
        
        # Placeholder vector
        vector = [0.1] * 384
        
        index.upsert(
            vectors=[{
                "id": book_id,
                "values": vector,
                "metadata": {
                    "type": "book",
                    "theme": book_data['theme'],
                    "pages_count": len(book_data['pages']),
                    "user_name": book_data['userName'],
                    "completed_at": book_data['completedAt'],
                    "summary": summary
                }
            }]
        )
        
        print(f"✅ Book saved to Pinecone: {book_id}")
    except Exception as e:
        print(f"❌ Error saving book to Pinecone: {e}")

