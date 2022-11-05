from __future__ import print_function

import praw
from datetime import datetime


reddit = praw.Reddit(
    client_id="3T-oFZPuLmWWWqtPTENRww",
    client_secret="F61a4n-kI7gyp881dHS8HPuwh8p27A",
    user_agent="my user agent",
)

subreddit = reddit.subreddit("india")

for post in subreddit.new(limit=200):
    title_lower = post.title.lower()
    if title_lower.__contains__('sadhguru'):
        print("post.title")
    print("--------------------------")
    commentTitle = post.title

    post.comments.replace_more(limit=None)
    comment_queue = post.comments[:]
    while comment_queue:
        comment = comment_queue.pop(0)
        comment_lower = comment.body.lower()
        if comment_lower.__contains__('sadhguru'):
            print("----------")
            print(datetime.fromtimestamp(comment.created_utc))
            commentDateTime = datetime.fromtimestamp(comment.created_utc)
            print(comment.body)
            commentBody = comment.body
            print("www.reddit.com" + comment.permalink)
        comment_queue.extend(comment.replies)










