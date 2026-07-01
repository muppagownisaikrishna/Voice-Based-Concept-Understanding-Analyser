from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(reference, response):

    emb1 = model.encode(reference, convert_to_tensor=True)

    emb2 = model.encode(response, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2)

    return float(similarity)