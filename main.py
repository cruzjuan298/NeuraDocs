import sys
import faiss #for vector database search of ragbot
from fastapi import FastAPI # for creating api 
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM #hugging face tranaformers library
from sentence_transformers import SentenceTransformer, util #imports tool for generating embeddings
import numpy as np

'''
#uses the Autokenizer to convert raw text/prompts to tokens which the pre trained model can understand
tokernizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

input = tokernizer("What is the capital of France?", return_tensors="pt")

print(input)

#importing a sequence to sequence model which is pre-trained on tasks like text sumarization, trnaslation, and q and a 
#no need to know tokenizer type for a specfic model because the imported libs load the corrext tokenizer based on model name/path
model1 = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

inputs = tokernizer("Translate English to French: What is your name?", return_tensors="pt")
outputs = model1.generate(**inputs)

print(tokernizer.decode(outputs[0], skip_special_tokens=True))

#loads a pre trained model that generates embeddings based on text or paragraphs
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = ["This is a test sentence", "This is another example"]
embeddings = model.encode(sentences)
'''
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

file_embeddings_npa = np.array(file_embeddings)

query = input("Please enter a query about the docs provided. The most relevant doc will be provided.")

query_embedding = model.encode(query)
def get_relevant_file(query_embedding, file_embeddings, file_name):
    similarities = util.cos_sim(query_embedding, file_embeddings)
    mos_rel_index = np.argmax(similarities)

    return file_name[mos_rel_index], similarities[mos_rel_index].item()

most_rel_file = get_relevant_file(query_embedding, file_embeddings, files)

