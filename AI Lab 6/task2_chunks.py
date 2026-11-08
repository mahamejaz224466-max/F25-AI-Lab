import re

def word_spans(text):
    return [(match.start(), match.end()) for match in re.finditer(r"\S+", text)]

def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")

    spans = word_spans(text)
    result = []
    step = size - overlap

    for i in range(0, len(spans), step):
        j = min(i + size, len(spans))
        result.append((offset + spans[i][0], offset + spans[j - 1][1]))
        if j == len(spans):
            break

    return result

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("Size must be positive.")

    cuts = [0] + [m.end() for m in re.finditer(r"[.!?]\s+", text)] + [len(text)]
    output = []
    pending = None
    count = 0

    for a, b in zip(cuts, cuts[1:]):
        segment = text[a:b]
        number_words = len(segment.split())

        if number_words == 0:
            continue

        if number_words > size:
            if pending is not None:
                output.append(pending)
            output.extend(windows(segment, size, 0, a))
            pending = None
            count = 0
        elif pending is not None and count + number_words <= size:
            pending = (pending[0], b)
            count += number_words
        else:
            if pending is not None:
                output.append(pending)
            pending = (a, b)
            count = number_words

    if pending is not None:
        output.append(pending)

    return output

def make_chunks(docs, strategy):
    result = []

    for doc_id, text in docs.items():
        if strategy == "sentence":
            spans = sentence_chunks(text, 40)
        elif strategy in ("0", "10"):
            spans = windows(text, 40, int(strategy))
        else:
            raise ValueError("Strategy must be 0, 10, or sentence.")

        for i, (start, end) in enumerate(spans):
            result.append({
                "id": doc_id + ":" + str(i),
                "doc": doc_id,
                "source": doc_id + ".txt",
                "start": start,
                "end": end,
                "text": text[start:end]
            })

    return result

if __name__ == "__main__":
    assert windows("") == []
    assert windows("short text") == [(0, 10)]

    try:
        windows("a b", 2, 2)
    except ValueError:
        print("Invalid overlap test passed.")
    else:
        raise AssertionError("Invalid overlap was accepted.")

    long_sentence = " ".join(["word"] * 95) + "."
    long_chunks = sentence_chunks(long_sentence)
    assert all(len(long_sentence[a:b].split()) <= 40 for a, b in long_chunks)

    with open("corpus.json", encoding="utf-8") as f:
        import json
        docs = json.load(f)

    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        for chunk in chunks:
            assert chunk["text"] == docs[chunk["doc"]][chunk["start"]:chunk["end"]]
        print(strategy, "chunks:", len(chunks))
