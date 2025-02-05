from services.embedding import model 
from services.storage import index

def find_best_match(query):
    query_embedding = model.encode(query).astype("float32").reshape(1, -1)
    _, cloest_id = index.search(query_embedding, k=1)
    return cloest_id[0][0]