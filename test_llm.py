from src.rag.rag_pipeline import query

if __name__ == "__main__":
    result = query("What are the Clio Awards?")
    print("Answer:", result.get("answer", "No answer"))
    print("Sources:", result.get("sources", []))
