from sentence_transformers import SentenceTransformer

from core.nlp.embeddings import Embeddings
from utils.configs import get_embedding_model


class SentenceTransformerEmbeddings(Embeddings):

    def __init__(self):
        super().__init__()
        print(f"Using {get_embedding_model()} to generate embeddings...")
        self.model = SentenceTransformer(get_embedding_model())
        self.model.max_seq_length = 512

    def get_word_count(self):
        return 200

    def get_prev_snippet_overlap_word_count(self):
        return 50

    def get_embeddings(self, normalized_texts):
        embeddings = self.model.encode(normalized_texts, normalize_embeddings=True)
        return embeddings
