import sys
import faiss #for vector database search of ragbot
from fastapi import FastAPI # for creating api 
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM #hugging face tranaformers library
from sentence_transformers import SentenceTransformer, util #imports tool for generating embeddings
import numpy as np

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

files_to_index = {}
sentence_mappings = {}
sentence_indexes = {}

d = model.get_sentence_embedding_dimension() ## getting embedding size
file_index = faiss.IndexFlatL2(d)

for i, file in enumerate(sys.argv[1:]):
    try:
        with open(file, encoding="UTF-8") as f:
            sentences = f.readlines()
            full_content = " ".join(sentences)

        ##### FILE LEVEL INDEXING ######
        file_embed = model.encode(full_content).astype("float32")
        files_to_index[i] = file ## store mapping
        file_index.add(file_embed.reshape(1, -1))

        ##### SENTENCE LEVEL INDEXING #######
        sentence_embeddings = model.encode(sentences).astype("float32")

        if sentence_embeddings.shape[1] != d:
            raise ValueError(f"Sentence embeddings have incorrect dimension{sentence_embeddings.shape[1]} instead of {d}")

        sent_index = faiss.IndexFlatL2(d)
        sent_index.add(sentence_embeddings)

        #Storing sentence level faiss index and sentences
        sentence_indexes[file] = sent_index
        sentence_mappings[file] = sentences

        print(f"Processed: {file}")

    except FileNotFoundError:
        print("No file found with that name.")
        continue
    except ValueError as e:
        print(e)
        continue

def get_relevant_file(query_embedding):
    _, closest_ids = file_index.search(query_embedding, k=1)
    most_rel_index = closest_ids[0][0]
    return files_to_index[most_rel_index]

def get_query_answer(query_embedding, file_name):
    if file_name not in sentence_indexes:
        return "Error: No sentence index found for the file."

    _, sentence_id = sentence_indexes[file_name].search(query_embedding, k=1)
    
    if sentence_id.size == 0:
        return "No relevant sentence found"
    
    most_rel_sentence = sentence_mappings[file_name][sentence_id[0][0]]
    return most_rel_sentence
        
def main():
    query = input("Please enter a query about the docs provided:")
    query_embedding = model.encode(query).astype("float32").reshape(1, -1) ##converting query to compt. type

    relevant_file_index = get_relevant_file(query_embedding)
    relevant_content = get_query_answer(query_embedding, relevant_file_index)
    print(f"\n Most relevant content: {relevant_content}")

if __name__ == "__main__":
    main()