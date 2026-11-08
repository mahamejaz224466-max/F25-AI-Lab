def retrieval_metrics(rankings, relevant):
    hits = []
    reciprocal_ranks = []

    for ids, good_ids in zip(rankings, relevant):
        ranks = []
        for rank, chunk_id in enumerate(ids[:3], 1):
            if chunk_id in good_ids:
                ranks.append(rank)

        hits.append(bool(ranks))
        reciprocal_ranks.append(1 / ranks[0] if ranks else 0)

    return sum(hits) / len(hits), sum(reciprocal_ranks) / len(reciprocal_ranks)


rankings = [["a", "b", "c"], ["c", "a", "b"], ["x", "y", "z"]]
relevant = [{"a"}, {"a"}, {"a"}]

hit, mrr = retrieval_metrics(rankings, relevant)
print(f"Hit@3={hit:.3f}; MRR@3={mrr:.3f}")

assert abs(hit - 2/3) < 1e-9
assert abs(mrr - 0.5) < 1e-9
