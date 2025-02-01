import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

d = model.get_sentence_embedding_dimension()
file_index = faiss.IndexFlatL2(d)
file_to_index = {} #mapping file index to filename
sentence_mapping = {} #mapping file(name) to setences
sentence_indexes = {} #sentence-level FAISS indexes
