import os
from dotenv import load_dotenv
import pinecone
import sys

def setup_pinecone_database():
    """Setup and verify Pinecone database configuration"""
    
    print("🚀 Starting Pinecone database setup...")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("PINECONE_API_KEY")
    
    # Verify API key is loaded
    if not api_key:
        print("❌ Error: PINECONE_API_KEY not found in environment variables")
        print("Please check your .env file contains: PINECONE_API_KEY=your_key_here")
        return False
    
    print("✅ API key loaded successfully")
    
    try:
        # Initialize Pinecone client
        print("🔌 Initializing Pinecone client...")
        pc = pinecone.Pinecone(api_key=api_key)
        print("✅ Pinecone client initialized")
        
        # List existing indexes
        print("📋 Checking existing indexes...")
        indexes = pc.list_indexes()
        print(f"Found {len(indexes)} indexes:")
        for idx in indexes:
            print(f"  - {idx.name} (dimension: {idx.dimension})")
        
        # Check if storyindex exists
        index_name = "storyindex"
        index_exists = any(idx.name == index_name for idx in indexes)
        
        if not index_exists:
            print(f"⚠️  Index '{index_name}' not found. Creating it...")
            # Create index with appropriate dimensions for embeddings
            pc.create_index(
                name=index_name,
                dimension=1024,  # Using 1024 dimensions to match existing index
                metric="cosine",
                spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
            )
            print(f"✅ Index '{index_name}' created successfully")
        else:
            print(f"✅ Index '{index_name}' already exists")
            # Get the actual dimension of the existing index
            existing_index = next(idx for idx in indexes if idx.name == index_name)
            actual_dimension = existing_index.dimension
            print(f"📏 Index dimension: {actual_dimension}")
        
        # Connect to the index
        print(f"🔗 Connecting to index '{index_name}'...")
        index = pc.Index(index_name)
        
        # Get index stats
        stats = index.describe_index_stats()
        print(f"📊 Index stats: {stats.total_vector_count} vectors")
        
        # Test with sample data
        print("🧪 Testing with sample data...")
        # Use the actual dimension of the index
        vector_dimension = existing_index.dimension if index_exists else 1024
        test_vectors = [
            {"id": "test_1", "values": [0.1] * vector_dimension, "metadata": {"title": "Test Story 1", "type": "test"}},
            {"id": "test_2", "values": [0.2] * vector_dimension, "metadata": {"title": "Test Story 2", "type": "test"}}
        ]
        
        # Upsert test data
        index.upsert(vectors=test_vectors)
        print("✅ Test data uploaded successfully")
        
        # Query test data
        query_vector = [0.1] * vector_dimension
        results = index.query(vector=query_vector, top_k=2, include_metadata=True)
        print("🔍 Query test results:")
        for match in results.matches:
            print(f"  - ID: {match.id}, Score: {match.score:.4f}, Metadata: {match.metadata}")
        
        # Clean up test data
        print("🧹 Cleaning up test data...")
        index.delete(ids=["test_1", "test_2"])
        print("✅ Test data cleaned up")
        
        print("\n🎉 Pinecone database setup completed successfully!")
        print(f"✅ Index '{index_name}' is ready for use")
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        print("Please check your API key and network connection")
        return False

if __name__ == "__main__":
    success = setup_pinecone_database()
    if not success:
        sys.exit(1)

