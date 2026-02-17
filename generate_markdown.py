import os
from datetime import datetime
from bot import generate_sw_comment  # your function from bot.py

# === CONFIG ===
TOPICS = [
    "Dario Amodei",
    "Sam Altman",
    "OpenAI",
    "Anthropic",
    "Andrej Karpathy",
    "Grok"
]
DAILY_LIMIT = 2  # max posts per day

# === MOCK NEWS FETCHER ===
# Replace this with your RSS fetcher / API
def fetch_news(topics, limit=DAILY_LIMIT):
    """
    Fetch news for given topics. 
    Returns a list of dicts: [{"title": ..., "summary": ..., "url": ...}, ...]
    """
    # Example: dummy news for testing
    return [
        {
            "title": "Dario Amodei joins OpenAI",
            "summary": "Former Anthropic co-founder moves to OpenAI to lead AI safety projects.",
            "url": "https://news.example.com/dario-amodei"
        },
        {
            "title": "Sam Altman talks AI regulation",
            "summary": "OpenAI CEO discusses safety and governance in AI at a conference.",
            "url": "https://news.example.com/sam-altman"
        }
    ][:limit]

# === MAIN SCRIPT ===
def main():
    articles = fetch_news(TOPICS, DAILY_LIMIT)

    if not articles:
        print("No news articles found for today.")
        return

    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    output_file = f"news-{today_str}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Swetlana Bot - Daily Commentary {today_str}\n\n")

        for article in articles:
            comment = generate_sw_comment(article["title"], article["summary"], article.get("url", ""))
            f.write(f"## {article['title']}\n\n")
            f.write(f"[Read full article here]({article['url']})\n\n")
            f.write(f"{comment}\n\n---\n\n")

    print(f"Daily file generated: {output_file}")


if __name__ == "__main__":
    main()
