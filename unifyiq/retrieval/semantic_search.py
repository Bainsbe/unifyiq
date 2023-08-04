from core.vectordb.milvus import Milvus

from utils.configs import get_env

if get_env() == "prod":
    vectors_store = Milvus()
    vectors_store.initialize_search()
else:
    print(get_env() + " env, skipping initialization of milvus")

def semantic_search(query):
    top_k_results = vectors_store.search(query, 2)
    return top_k_results

# semantic_search("what is the status of project skynet?")
# semantic_search("What was the reason for the high database load?")
