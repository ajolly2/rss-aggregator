from flask import Flask, jsonify
import feedparser

app = Flask(__name__)

RSS_FEEDS = [
    "https://sports.yahoo.com/general/news/rss/",
    "https://www.espn.com/espn/rss/news"
]

@app.route("/rss")
def fetch_rss():
    all_items = []
    
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            all_items.append({
                "title": entry.title,
                "link": entry.link
            })

    return jsonify(all_items)  # ✅ Ensure it returns JSON

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
