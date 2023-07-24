# Read the list of adapters from the database and launch them
from datetime import datetime

from pymilvus.orm import utility

from core.nlp.snippet_gen import update_embeddings
from core.vectordb.milvus import Milvus, MILVUS_COLLECTION_NAME
from utils.configs import delete_index_always
from utils.database import unifyiq_config_db
from utils.file_utils import get_core_output_path_from_config
from utils.storage import storage_util


def init_vector_store():
    vectors_store = Milvus()
    if delete_index_always():
        print("Dropping collection")
        utility.drop_collection(MILVUS_COLLECTION_NAME)
    vectors_store.initialize_indexer()
    return vectors_store


def update_index(vectors_store, source_config, current_date_hod):
    output_storage = storage_util.get_storage_instance()
    print(f"Generating embeddings for {source_config.name} - {source_config.connector_type}")
    update_embeddings(source_config, output_storage, current_date_hod)
    print(f"Indexing to Milvus - {get_core_output_path_from_config(source_config, current_date_hod)}/embeddings.pkl")
    vectors_store.insert(f"{get_core_output_path_from_config(source_config, current_date_hod)}/embeddings.pkl")
    print(f"Index Updated")


if __name__ == '__main__':
    source_configs = unifyiq_config_db.get_fetcher_configs()
    # TODO Assumes unifyiq will run no frequently than once a day
    current_date_hod = datetime.now().strftime("%Y-%m-%dT00-00-00")
    vector_store = init_vector_store()
    for source_config in source_configs:
        update_index(vector_store, source_config, current_date_hod)
    pass
