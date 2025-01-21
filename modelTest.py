from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

responseQueries = ["Our cancelation policy is valid up until 4 weeks after your purchase date.", "If you would like to delete your account, please visit your dashboard and click on the option to delete your account.", "I am a helpful chetbot who is here to asissts you woth any questions you may have!" ]
questionQueries = ["Would you like to see if you qualify for a cancelation?", "How are you doing today?", "How may I help you today"]

embeddingResponses = model.encode(responseQueries)
embeddingQuestions = model.encode(questionQueries)


similartiesResponses = model.similarity(embeddingQuestions, embeddingResponses)
print(similartiesResponses)