# Read the list of adapters from the database and launch them
from datetime import datetime

from pymilvus.orm import utility

from core.nlp.snippet_gen import update_embeddings
from core.vectordb.milvus import Milvus, MILVUS_COLLECTION_NAME
from utils.configs import delete_index_always
from utils.database import unifyiq_config_db
from utils.file_utils import get_core_output_path_from_config

configs = unifyiq_config_db.get_fetcher_configs()
# TODO Assumes unifyiq will run no frequently than once a day
current_date_hod = datetime.now().strftime("%Y-%m-%dT00-00-00")

vectors_store = Milvus()
if delete_index_always():
    print("Dropping collection")
    utility.drop_collection(MILVUS_COLLECTION_NAME)
vectors_store.initialize_indexer()
for config in configs:
    print(f"Generating embeddings for {config.name} {config.connector_platform} - {config.connector_type}")
    update_embeddings(config, current_date_hod)
    print(f"Indexing to Milvus - {get_core_output_path_from_config(config, current_date_hod)}/embeddings.pkl")
    vectors_store.insert(f"{get_core_output_path_from_config(config, current_date_hod)}/embeddings.pkl")
    print(f"Index Updated")
