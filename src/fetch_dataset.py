import requests
import datetime
import csv

def fetch_posts(subreddit, months):
    base_url = "https://api.pullpush.io/reddit/search/submission"
    current_time = datetime.datetime.utcnow()
    results = []

    for month in range(months):
        before = int(current_time.timestamp())
        after = int((current_time - datetime.timedelta(days=30)).timestamp())
        
        current_time -= datetime.timedelta(days=30)

        params = {
            'subreddit': subreddit,
            'before': before,
            'after': after,
            'size': 1000
        }
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            results.extend(data)
        else:
            print(f"Failed to fetch data for month {month + 1}: {response.status_code}")

    return results

def save_to_csv(data, filename):
    headers = [
        "name", "title", "selftext", "author", "created_utc", "score", 
        "num_comments", "subreddit", "link_flair_text", "url"
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for post in data:
            selftext = post.get('selftext', '').replace('\n', ' ').replace('\r', ' '),
            if selftext[0] == "[removed]": continue
            row = [
                post.get('name', 'None'),
                post.get('title', '').replace('\n', ' ').replace('\r', ' '),
                post.get('selftext', '').replace('\n', ' ').replace('\r', ' '),
                post.get('author', 'None'),
                post.get('created_utc', 'None'),
                post.get('score', 0),
                post.get('num_comments', 0),
                post.get('subreddit', 'None'),
                post.get('link_flair_text', 'None'),
                post.get('url', 'None')
            ]
            writer.writerow(row)

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch and save Reddit posts.')
    parser.add_argument('subreddit', type=str, help='The subreddit to fetch posts from')
    parser.add_argument('years', type=int, help='The number of years of posts to fetch')
    parser.add_argument('filename', type=str, help='The filename to save the posts to')

    args = parser.parse_args()

    months = args.years * 12

    posts = fetch_posts(args.subreddit, months)
    save_to_csv(posts, args.filename)
    print(f"Data saved to {args.filename}")