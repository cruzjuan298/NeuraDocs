import numpy as np

def blobToEmbedding(embedding_blob: bytes) -> np.ndarray:

    embedding_array = np.frombuffer(embedding_blob, dtype=np.float32).reshape(1, -1)

    return embedding_array