from core.vectordb.milvus import Milvus

vectors_store = Milvus()
vectors_store.initialize_search()


def semantic_search(query):
    top_k_results = vectors_store.search(query, 2)
    return top_k_results

# semantic_search("what is the status of project skynet?")
# semantic_search("What was the reason for the high database load?")
