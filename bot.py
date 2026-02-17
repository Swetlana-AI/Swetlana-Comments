import os
from openai import OpenAI

# Load secrets from GitHub Actions environment
client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ.get("BASE_URL")  # optional if using default
)

MODEL = os.environ["MODEL"]
SYSTEM_PROMPT = os.environ["SYSTEM_PROMPT"]  # br. prompt

import os

def load_docs(knowledge_folder="knowledge"):
    """Load all .md files in the knowledge folder."""
    text = ""
    for root, _, files in os.walk(knowledge_folder):
        for f in files:
            if f.endswith(".md"):
                with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                    text += file.read() + "\n\n"
    return text

DOCS = load_docs()


def generate_sw_comment(title: str, summary: str) -> str:
    """
    Generate a Swetlana-style comment for a news item.
    """
    prompt = f"""
{SYSTEM_PROMPT}

### Knowledge Base
{DOCS}

### News Item
Title: {title}
Summary: {summary}

Provide a concise, insightful, and reflective commentary in Swetlana's style.
"""
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return resp.choices[0].message.content.strip()


# Example usage for local testing
if __name__ == "__main__":
    test_title = "Dario Amodei joins OpenAI"
    test_summary = "Former Anthropic co-founder moves to OpenAI to lead AI safety projects."
    print(generate_sw_comment(test_title, test_summary))
