import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Retriever:
    def __init__(self, records, backend="tfidf"):
        if not records or any(not r["text"].strip() for r in records):
            raise ValueError("Please provide non-empty records.")

        self.records = records
        self.backend = backend
        texts = [r["text"] for r in records]

        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer()
            self.matrix = self.vectorizer.fit_transform(texts)
        elif backend == "embedding":
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
            )
            self.check_length(texts)
            self.matrix = self.model.encode(
                texts, normalize_embeddings=True
            )
        else:
            raise ValueError("Backend must be tfidf or embedding.")

    def check_length(self, texts):
        for text in texts:
            token_ids = self.model.tokenizer(
                text, truncation=False
            )["input_ids"]
            if len(token_ids) > self.model.max_seq_length:
                raise ValueError("Text is longer than the model limit.")

    def search(self, query, k=3, filters=None):
        if not query.strip() or k <= 0:
            return []

        if self.backend == "tfidf":
            query_vector = self.vectorizer.transform([query])
            if query_vector.nnz == 0:
                return []
            scores = (query_vector @ self.matrix.T).toarray()[0]
        else:
            self.check_length([query])
            query_vector = self.model.encode(
                [query], normalize_embeddings=True
            )[0]
            scores = self.matrix @ query_vector

        allowed = []
        for i, record in enumerate(self.records):
            keep = True
            for key, value in (filters or {}).items():
                if record.get(key) != value:
                    keep = False
            if keep:
                allowed.append(i)

        ranked = sorted(allowed, key=lambda i: (-float(scores[i]), i))
        return [(self.records[i], float(scores[i])) for i in ranked[:k]]

def show_hits(hits):
    if not hits:
        print("No matching records.")
    for record, score in hits:
        print(record["id"], "score=" + str(round(score, 3)))
        print(record["text"])
