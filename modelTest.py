from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

try: 
    with open("mockFAQ.txt", "r") as file:
        lines = file.readlines()

except FileNotFoundError:
    print("No file found")

questions = []
answers = []

for i in range(len(lines) - 1):
    if "?" in lines[i]:
        question = lines[i].strip().split("**")[1]
        answer = lines[i + 1].strip()
        questions.append(question)
        answers.append(answer)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

embeddingQuestions = model.encode(questions) #encoding data to embeddings for further analysis/retrival
embeddingResponses = model.encode(answers)

#similartiesResponses = model.similarity(embeddingQuestions, embeddingResponses) #computing similarity scores. May not be useful for search and retrival

similarties_cos = cosine_similarity(embeddingQuestions, embeddingResponses)

#print(similartiesResponses)
print(similarties_cos)