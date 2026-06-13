import requests

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    return response.json()["response"]

def main():
    print(f"Local LLM Assistant ({MODEL})")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower().strip() in {"exit", "quit"}:
            break

        prompt = f"""
You are a helpful assistant.
Explain clearly and concisely.

Question:
{question}
"""

        answer = ask_llm(prompt)
        print(f"\nAssistant: {answer}\n")

if __name__ == "__main__":
    main()