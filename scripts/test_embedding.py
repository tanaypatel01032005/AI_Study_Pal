import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.embeddings.service import EmbeddingService

def test():
    print("Testing Embedding Service (API based)...")
    emb = EmbeddingService.generate_embedding("What is calculus?")
    print(f"Generated embedding of size {len(emb)}")
    if len(emb) == 384:
        print("Success: Embedding size is correct.")
    else:
        print(f"Warning: Unexpected embedding size {len(emb)}")

if __name__ == "__main__":
    test()
