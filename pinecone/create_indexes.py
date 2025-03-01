import os
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def create_indexes(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        namespace="default",
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
        deletion_protection="disabled",
        tags={
            "environment": "development"
        }
    )
    print(f"Index {index_name} created successfully. {pc.describe_index(index_name)}")
    
def delete_indexes(index_name):
    pc.delete_index(index_name)
    print(f"Index {index_name} deleted successfully.")


if __name__ == "__main__":
    
# ==========================================================================
# Create book-index-1
# ==========================================================================

    create_indexes("book-index1")

# ==========================================================================
# Create book-index-1
# ==========================================================================

    create_indexes("book-index2")