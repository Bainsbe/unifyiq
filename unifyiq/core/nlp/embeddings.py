from abc import ABCMeta, abstractmethod


class Embeddings(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_word_count(self):
        pass

    @abstractmethod
    def get_prev_snippet_overlap_word_count(self):
        pass

    @abstractmethod
    def get_embeddings(self, normalized_texts):
        pass
