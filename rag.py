import json
import faiss
import numpy as np
from utils.embeddings import get_embedding

with open("data/faq.json") as f:
    data = json.load(f)

texts = [
    f"{item['location']} {item['type']} property {item['details']} {item['description']}"
    for item in data
]
embeddings = np.array([get_embedding(t) for t in texts])

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def retrieve(query):
    q_emb = np.array([get_embedding(query)])
    D, I = index.search(q_emb, k=2)

    results = [data[i] for i in I[0]]
    score = D[0][0]

    return results, score