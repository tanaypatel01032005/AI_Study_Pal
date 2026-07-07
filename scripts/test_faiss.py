import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.rag.vector_store import FAISSStore

def test():
    print("Testing FAISS Integration...")
    store = FAISSStore(dimension=384, index_path="test_index.bin")
    
    # Add dummy embeddings
    embeddings = [[0.1] * 384, [0.2] * 384, [0.9] * 384]
    ids = [1, 2, 3]
    
    store.add_embeddings(embeddings, ids)
    print(f"Added {len(embeddings)} vectors to index.")
    
    # Search
    query = [0.95] * 384
    results = store.search(query, top_k=2)
    print(f"Search results for [0.95]: {results}")
    
    if results and results[0][0] == 3:
        print("Success: FAISS search returned the closest vector correctly.")
    else:
        print("Warning: FAISS search did not return expected results.")
        
    if os.path.exists("test_index.bin"):
        os.remove("test_index.bin")

if __name__ == "__main__":
    test()
