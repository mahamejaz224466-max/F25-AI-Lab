import csv
import json
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from task2_chunks import make_chunks

def evidence_metrics(scores, chunks, questions):
    hits = []
    reciprocal_ranks = []

    for row, question in zip(scores, questions):
        if question["doc"] is None:
            continue

        top = np.argsort(-row, kind="stable")[:3]
        good_ranks = []

        for rank, index in enumerate(top, 1):
            chunk = chunks[index]
            if (chunk["doc"] == question["doc"]
                    and question["evidence"] in chunk["text"]):
                good_ranks.append(rank)

        hits.append(bool(good_ranks))
        reciprocal_ranks.append(1 / good_ranks[0] if good_ranks else 0)

    if not hits:
        return None, None

    return sum(hits) / len(hits), sum(reciprocal_ranks) / len(reciprocal_ranks)

def main():
    with open("corpus.json", encoding="utf-8") as file:
        docs = json.load(file)
    with open("queries.json", encoding="utf-8") as file:
        questions = json.load(file)

    for question in questions:
        if question["doc"] is not None:
            assert question["evidence"] in docs[question["doc"]]

    start = time.perf_counter()
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
    )
    print("Model load time:", round(time.perf_counter() - start, 3), "seconds")

    query_texts = [question["query"] for question in questions]
    logs = []

    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        chunk_texts = [chunk["text"] for chunk in chunks]

        token_lengths = [
            len(model.tokenizer(text, truncation=False)["input_ids"])
            for text in chunk_texts + query_texts
        ]
        if max(token_lengths) > model.max_seq_length:
            raise ValueError("Model input limit exceeded.")

        for method in ["tfidf", "embedding"]:
            start = time.perf_counter()

            if method == "tfidf":
                vectorizer = TfidfVectorizer()
                chunk_vectors = vectorizer.fit_transform(chunk_texts)
                query_vectors = vectorizer.transform(query_texts)
            else:
                chunk_vectors = model.encode(
                    chunk_texts, normalize_embeddings=True
                )
                query_vectors = model.encode(
                    query_texts, normalize_embeddings=True
                )

            encoding_time = time.perf_counter() - start

            start = time.perf_counter()
            if method == "tfidf":
                scores = (query_vectors @ chunk_vectors.T).toarray()
            else:
                scores = query_vectors @ chunk_vectors.T
            search_time = time.perf_counter() - start

            for split in ["dev", "test"]:
                indices = [
                    i for i, question in enumerate(questions)
                    if question["split"] == split
                ]
                metric_result = evidence_metrics(
                    scores[indices], chunks, [questions[i] for i in indices]
                )
                print(
                    strategy, method, split,
                    "Hit@3/MRR@3:", metric_result,
                    "chunk count:", len(chunks),
                    "encode/index time:", round(encoding_time, 4),
                    "search time:", round(search_time, 4)
                )

            for row, question in zip(scores, questions):
                top_indices = np.argsort(-row, kind="stable")[:3]
                for rank, index in enumerate(top_indices, 1):
                    chunk = chunks[index]
                    logs.append({
                        "strategy": strategy,
                        "method": method,
                        "query": question["query"],
                        "split": question["split"],
                        "answerable": question["doc"] is not None,
                        "rank": rank,
                        "score": float(row[index]),
                        "chunk_id": chunk["id"],
                        "doc": chunk["doc"],
                        "start": chunk["start"],
                        "end": chunk["end"],
                        "text": chunk["text"]
                    })

    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(logs[0].keys()))
        writer.writeheader()
        writer.writerows(logs)

    print("Saved retrieval_log.csv")

if __name__ == "__main__":
    main()
