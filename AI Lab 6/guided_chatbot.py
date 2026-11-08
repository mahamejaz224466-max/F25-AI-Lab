from lab6_search import Retriever

FAQ = [
    {
        "id": "faq:password",
        "question": "How do I reset my password?",
        "answer": "Use the recovery link on the login page.",
        "source": "it_help.txt"
    },
    {
        "id": "faq:submit",
        "question": "Where do I submit my assignment?",
        "answer": "Use the assignment upload page in the learning portal.",
        "source": "assessment.txt"
    },
    {
        "id": "faq:late",
        "question": "Can illness justify a late submission?",
        "answer": "Request an extension with medical evidence before the deadline.",
        "source": "handbook.txt"
    },
    {
        "id": "faq:library",
        "question": "When does the library open?",
        "answer": "The synthetic example library opens at 8 AM.",
        "source": "library_example.txt"
    },
    {
        "id": "faq:email",
        "question": "How can I contact the help desk?",
        "answer": "Send a message to helpdesk@example.edu.",
        "source": "it_help.txt"
    }
]

def build_bot(backend="tfidf"):
    records = []
    for faq in FAQ:
        record = dict(faq)
        record["text"] = faq["question"] + " " + faq["answer"]
        records.append(record)
    return Retriever(records, backend)

def reply(engine, query):
    if not query.strip():
        return "Please enter a question."

    for faq in FAQ:
        if query.strip().casefold() == faq["question"].casefold():
            return faq["answer"] + " [source: " + faq["source"] + "]"

    hits = engine.search(query)
    if not hits:
        return "No matching FAQ. Please contact the help desk."

    lines = ["Possible matches; choose or rephrase your question:"]
    for record, score in hits:
        lines.append(record["question"] + " (similarity " + str(round(score, 3)) + ")")
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["tfidf", "embedding"], default="tfidf")
    args = parser.parse_args()

    engine = build_bot(args.backend)
    print("FAQ assistant. Type exit to stop.")

    while True:
        try:
            query = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break

        if query.strip().lower() == "exit":
            break

        print("Bot:", reply(engine, query))
