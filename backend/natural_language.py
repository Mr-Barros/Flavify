# natural_language.py

from torch import Tensor
from sentence_transformers import SentenceTransformer, util

# Encapsulamento dos atributos e disponibilização apenas das funções de acesso
__all__ = ["sentence_similarity"]

def sentence_similarity(sentence1: str, sentence2: str) -> float:
    """
    Avalia a similaridade entre duas frases utilizando NLP.

    Args:
        sentence1 (str): primeira frase.
        sentence2 (str): segunda frase.

    Returns:
        (float): valor que indica o grau de similaridade entre as frases, entre 0 e 1.
    """

    model: SentenceTransformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    emb1: Tensor = model.encode(sentence1, convert_to_tensor=True) # pyright: ignore[reportUnknownMemberType]
    emb2: Tensor = model.encode(sentence2, convert_to_tensor=True) # pyright: ignore[reportUnknownMemberType]

    similarity: float = util.cos_sim(emb1, emb2).item() # pyright: ignore[reportUnknownMemberType]
    similarity = max(similarity, 0)
    
    return similarity
