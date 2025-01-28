import sys
import faiss #for vector database search of ragbot
from fastapi import FastAPI # for creating api 
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM #hugging face tranaformers library
from sentence_transformers import SentenceTransformer, util #imports tool for generating embeddings
import numpy as np

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

file_embeddings = []
files = []

files_num = len(sys.argv)
for i in range(1, files_num):
    try:
        with open(sys.argv[i], encoding="UTF-8")as inputFile:
            file_content = inputFile.read()
            embedding = model.encode(file_content)
            file_embeddings.append(embedding)
            files.append(sys.argv[i])
    except FileNotFoundError:
        print("No file found with that name.")

file_embeddings_npa = np.vstack(file_embeddings)

def get_relevant_file_index(query_embedding, file_embeddings):
    similarities = util.cos_sim(query_embedding, file_embeddings)

    similarities_array = similarities.numpy()

    mos_rel_index = np.argmax(similarities_array)

    return mos_rel_index

def get_query_answer(query_embedding, file_index):
    file_name = files[file_index]

    file_sentences = []

    with open(file_name, encoding="UTF-8") as inputFile:
        file_sentences = inputFile.readlines()

    sentences_embeddings = model.encode(file_sentences)

    similarties = util.cos_sim(query_embedding, sentences_embeddings)
    similarties_npar = similarties.numpy()

    most_rel_index  = np.argmax(similarties_npar)
    most_rel_sentence = file_sentences[most_rel_index]

    return most_rel_sentence
        
def main():
    query = input("Please enter a query about the docs provided:")
    query_embedding = model.encode(query)

    relevant_file_index = get_relevant_file_index(query_embedding, file_embeddings)
    relevant_content = get_query_answer(query_embedding, relevant_file_index)
    print(f"\n Most relevant content: {relevant_content}")

if __name__ == "__main__":
    main()