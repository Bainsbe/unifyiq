from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

from core.nlp.sentence_transformer_embeddings import SentenceTransformerEmbeddings
from core.vectordb.vector_db import VectorDB
from utils.configs import get_milvus_uri, get_embedding_dimension
from utils.constants import ID, SOURCE, TEXT, EMBEDDINGS, DISTANCE
from utils.text_utils import normalize

MILVUS_COLLECTION_NAME = "unifyiq"


class Milvus(VectorDB):

    def __init__(self):
        super().__init__()
        self.embeddings_gen = None
        connections.connect("default", address=get_milvus_uri())
        if utility.has_collection(MILVUS_COLLECTION_NAME):
            self.collection = Collection(MILVUS_COLLECTION_NAME)
        else:
            self.initialize_indexer()

    def initialize_search(self):
        self.collection.load()
        self.embeddings_gen = SentenceTransformerEmbeddings()

    def initialize_indexer(self):
        if not utility.has_collection(MILVUS_COLLECTION_NAME):
            fields = [
                FieldSchema(name=ID, dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
                FieldSchema(name=TEXT, dtype=DataType.VARCHAR, max_length=4096),
                FieldSchema(name=SOURCE, dtype=DataType.VARCHAR, max_length=2048),
                FieldSchema(name=EMBEDDINGS, dtype=DataType.FLOAT_VECTOR, dim=get_embedding_dimension())
            ]
            schema = CollectionSchema(fields, "UnifyIQ Knowledge Assistant for Tech Teams")
            self.collection = Collection(MILVUS_COLLECTION_NAME, schema)
            index = {
                "index_type": "IVF_FLAT",
                "metric_type": "IP",
                "params": {"nlist": 128},
            }
            # index = {
            #     "index_type": "HNSW",
            #     "metric_type": "IP",
            #     "params": {"efConstruction": 512, "M": 32},
            # }
            self.collection.create_index(EMBEDDINGS, index)
        else:
            self.collection = Collection(MILVUS_COLLECTION_NAME)

    def insert(self, file_name):
        entities = self.load_embeddings(file_name)
        # insert if there are any entries
        if entities and entities[0]:
            self.collection.insert(entities)
            self.collection.flush()

    def search(self, query, top_n):
        search_params = {"metric_type": "IP", "params": {"nprobe": 20}, "offset": 0}
        # search_params = {"metric_type": "IP", "params": {"ef": 100}, "offset": 5}
        embeddings = self.embeddings_gen.get_embeddings(normalize(query))
        results = self.collection.search(
            data=[embeddings],
            anns_field=EMBEDDINGS,
            param=search_params,
            limit=min(top_n, 5),
            expr=None,
            # set the names of the fields you want to retrieve from the search result.
            output_fields=[ID, SOURCE, TEXT],
            consistency_level="Strong"
        )
        hits = []
        for r in results[0]:
            hit = {ID: r.id, DISTANCE: r.distance, SOURCE: r.entity.get(SOURCE), TEXT: r.entity.get(TEXT)}
            hits.append(hit)
        return hits
