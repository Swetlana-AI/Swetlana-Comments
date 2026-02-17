import os
from datetime import datetime
from bot import generate_sw_comment

OUTPUT_FILE = "news.md"
TOPICS = ["Dario Amodei", "Sam Altman", "OpenAI", "Anthropic", "Andrej Karpathy", "Grok"]

# Mock: replace with your RSS fetch or other news source
def fetch_news(topics, limit=2):
    # For now, return 2 dummy news items for testing
    return [
        {"title": "Dario Amodei joins OpenAI",
         "summary": "Former Anthropic co-founder moves to OpenAI to lead AI safety projects."},
        {"title": "Sam Altman talks AI regulation",
         "summary": "OpenAI CEO discusses safety and governance in AI at a conference."}
    ][:limit]

def main():
    articles = fetch_news(TOPICS, limit=2)

    if not articles:
        articles = []

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Swetlana Bot - Daily Commentary {today_str}\n\n")
        for article in articles:
            comment = generate_sw_comment(article["title"], article["summary"])
            f.write(f"## {article['title']}\n\n")
            f.write(f"{comment}\n\n---\n\n")

if __name__ == "__main__":
    main()
