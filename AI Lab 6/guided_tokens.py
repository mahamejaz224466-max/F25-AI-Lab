import json
from task2_chunks import make_chunks
from lab6_search import Retriever

if __name__ == "__main__":
    with open("corpus.json", encoding="utf-8") as file:
        documents = json.load(file)

    chunks = make_chunks(documents, "sentence")
    engine = Retriever(chunks, "embedding")

    print("Document evidence chatbot. Type exit to stop.")

    while True:
        try:
            query = input("Question: ")
        except (EOFError, KeyboardInterrupt):
            break

        if query.strip().lower() == "exit":
            break

        hits = engine.search(query)
        if not hits:
            print("No candidate evidence. Please rephrase or ask a human.")
            continue

        print("Possible evidence:")
        for number, (record, score) in enumerate(hits, 1):
            print(number, record["id"], round(score, 3),
                  "characters", record["start"], record["end"])

        choice = input("Choose 1-3 to inspect, or press Enter to cancel: ")
        if not choice.isdigit() or not 1 <= int(choice) <= len(hits):
            print("No evidence selected. Please rephrase or ask a human.")
            continue

        record, score = hits[int(choice) - 1]
        print("Evidence:", record["text"])
        print("Source:", record["source"])
        print("Character offsets:", record["start"], record["end"])
