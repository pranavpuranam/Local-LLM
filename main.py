import requests

MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are a helpful assistant.
Explain clearly and concisely.
If you are unsure, say so.
"""

MAX_HISTORY_CHARS = 6000


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


def build_prompt(history: str, question: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Conversation so far:
{history}

User:
{question}

Assistant:
"""


def main():
    print(f"Local LLM Assistant ({MODEL})")
    print("Type 'exit' or 'quit' to quit.")
    print("Type '/clear' to clear conversation memory.\n")

    history = ""

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if question.lower() == "/clear":
            history = ""
            print("Conversation memory cleared.\n")
            continue

        if not question:
            continue

        prompt = build_prompt(history, question)

        try:
            answer = ask_llm(prompt)
        except requests.RequestException as e:
            print(f"\nError contacting Ollama: {e}\n")
            continue

        print(f"\nAssistant: {answer}\n")

        history += f"\nUser: {question}\nAssistant: {answer}\n"

        if len(history) > MAX_HISTORY_CHARS:
            history = history[-MAX_HISTORY_CHARS:]


if __name__ == "__main__":
    main()