import pandas as pd
import praw
import sys
from datetime import datetime
import config_helper as config_helper

SECRETS_FILE = 'pipeline_secrets.conf'


def extract_posts_data():
    reddit_service = _get_reddit_service()

    reddit_configs = config_helper.get_config_section('reddit')
    subreddit = reddit_service.subreddit(reddit_configs.get('subreddit'))
    posts_num = reddit_configs.get('posts_num')
    posts_num = int(posts_num) if posts_num.isdigit() else None

    submissions = subreddit.top(time_filter='day', limit=posts_num)

    submissions_list = []
    for s in submissions:
        s = vars(s)
        s = {k: str(v) for k, v in s.items()}
        submissions_list.append(s)
    print(f'Retrieved {len(submissions_list)} submissions from reddit')
    return submissions_list


def _get_reddit_service():
    reddit_configs = config_helper.get_config_section('reddit', SECRETS_FILE)

    try:
        return praw.Reddit(client_id=reddit_configs.get('client_id'),
                           client_secret=reddit_configs.get('client_secret'),
                           user_agent='reddit-etl-ukraine')
    except Exception as ex:
        print(f'Failed to connect to Reddit API: {ex}')
        sys.exit(1)


def transform_posts(posts_list):
    headers_list = ['id', 'title', 'score', 'num_comments', 'author',
                    'ups', 'upvote_ratio', 'total_awards_received',
                    'permalink', 'url', 'created_utc', 'is_video', 'over_18']
    posts_list = [{key: d[key] for key in headers_list} for d in posts_list]
    today = datetime.utcnow().strftime('%Y-%m-%d')
    for p in posts_list:
        # Add current date as insertion date
        p.update({"insertion_date": today})
        # Edit the permalink field to save the full URL
        p.update((k, f'https://reddit.com{v}') for k, v in p.items() if k == "permalink")
        # Convert time format
        p.update((k, datetime.utcfromtimestamp(float(v)).isoformat()) for k, v in p.items() if k == "created_utc")
    return posts_list


def save_to_csv(extracted_data):
    reddit_configs = config_helper.get_config_section('reddit')
    subreddit = reddit_configs.get('subreddit')
    extracted_data_df = pd.DataFrame(extracted_data)

    filename = f'/tmp/r_{subreddit}_{datetime.now().strftime("%Y%m%d")}.csv'
    extracted_data_df.to_csv(filename, index=False, encoding='utf-8')
