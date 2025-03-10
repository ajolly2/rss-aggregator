from flask import Flask, Response
import feedparser
import time

app = Flask(__name__)

# RSS feeds to aggregate
RSS_FEEDS = [
    "https://sports.yahoo.com/general/news/rss/",
    "https://www.espn.com/espn/rss/news"
]

def fetch_feeds():
    """Fetch and combine RSS feeds in alternating order."""
    parsed_feeds = [feedparser.parse(url).entries for url in RSS_FEEDS]
    combined_feed = []

    # Interleave articles (Yahoo, ESPN, Yahoo, ESPN...)
    max_len = max(len(feed) for feed in parsed_feeds)
    for i in range(max_len):
        for feed in parsed_feeds:
            if i < len(feed):
                combined_feed.append(feed[i])

    return combined_feed

@app.route("/")
def rss_feed():
    """Generate a combined RSS feed."""
    articles = fetch_feeds()

    rss_items = ""
    for item in articles:
        rss_items += f"""
        <item>
            <title>{item.title}</title>
            <link>{item.link}</link>
            <description>{item.get('summary', 'No description')}</description>
            <pubDate>{item.get('published', time.strftime("%a, %d %b %Y %H:%M:%S GMT"))}</pubDate>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
        <title>Combined Sports News</title>
        <link>#</link>
        <description>Latest news from Yahoo Sports and ESPN</description>
        {rss_items}
    </channel>
    </rss>
    """

    return Response(rss_feed, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
