import os
import feedparser
from datetime import datetime
from bot import generate_sw_comment  # import your function

# Topics to track
TOPICS = [
    "Dario Amodei",
    "Sam Altman",
    "OpenAI",
    "Anthropic",
    "Andrej Karpathy",
    "Grok"
]

# Google News RSS URL template
RSS_TEMPLATE = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

# Limit posts per run
MAX_POSTS = 2

# Output file
OUTPUT_FILE = "news.md"


def fetch_news(topics):
    articles = []
    for topic in topics:
        url = RSS_TEMPLATE.format(query=topic.replace(" ", "+"))
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Keep only the first paragraph of summary if available
            summary = entry.get("summary", entry.get("title", ""))
            first_para = summary.split("\n")[0].strip()
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": first_para
            })
    # Sort newest first
    articles.sort(key=lambda x: x.get("published_parsed", datetime.now()), reverse=True)
    return articles[:MAX_POSTS]


def main():
    articles = fetch_news(TOPICS)
    if not articles:
        print("No articles found.")
        return

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    content = f"# Swetlana Bot - Daily Commentary {date_str}\n\n"

    for article in articles:
        comment = generate_sw_comment(article["title"], article["summary"])
        content += f"## {article['title']}\n\n"
        content += f"{article['summary']}\n\n"
        content += f"**Swetlana Bot Commentary:**\n\n{comment}\n\n"
        content += f"[Read more]({article['link']})\n\n---\n\n"

    # Append to existing file or create if missing
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            old_content = f.read()
        content = content + old_content

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated {OUTPUT_FILE} with {len(articles)} new articles.")


if __name__ == "__main__":
    main()
