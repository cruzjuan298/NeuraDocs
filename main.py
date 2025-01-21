import faiss #for vector database search of ragbot
from fastapi import FastAPI # for creating api 
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM #hugging face tranaformers library
from sentence_transformers import SentenceTransformer #imports tool for generating embeddings

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

#embeddings is a high dimensional vector
print(embeddings)

