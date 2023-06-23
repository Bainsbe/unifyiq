import pickle
from abc import ABCMeta, abstractmethod

from utils.constants import ID, SOURCE, TEXT, EMBEDDINGS


class VectorDB(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def initialize_indexer(self):
        pass

    @abstractmethod
    def initialize_search(self):
        pass

    @abstractmethod
    def insert(self, file_name):
        pass

    def load_embeddings(self, file_name):
        with open(file_name, "rb") as fIn:
            snippets = pickle.load(fIn)
            entities = [
                snippets[ID],
                snippets[TEXT],
                snippets[SOURCE],
                snippets[EMBEDDINGS]
            ]
            return entities

    @abstractmethod
    def search(self, text, top_n):
        pass
