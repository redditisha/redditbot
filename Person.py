from __future__ import print_function

import praw
from datetime import datetime

import gspread
# from oauth2Client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from praw.models.reddit import submission

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'Keys.json'

reddit = praw.Reddit(
    client_id="3T-oFZPuLmWWWqtPTENRww",
    client_secret="F61a4n-kI7gyp881dHS8HPuwh8p27A",
    user_agent="my user agent",
)

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

credens = {
    "type": "service_account",
    "project_id": "redditbot-363109",
    "private_key_id": "a07629ebcbcecc27e45de1d21e72e065d2f4205a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDZ+QeKSHucxFTJ\nAhnGyvAaKq0JGejU5D1W8ESt5slAUBVP0JL6p0yMJlcPepveD86DtcQdrO48BfMv\nzJrE0DWpeIi1/qFaG62L+o30p2dtCLqBewzd2pZ2bEPZfyTa+NJU2QzGE9yjiB6B\nEzkLIvYKtNmdHVH/seaSzkXNOgbSXfwKbWbGBmLfuKFLAxWy2jGBUqX1sZaSYRIx\nnlnhvz/cCF8EogIqGYhYs8TK30oUq9Z4Q4LmHauBUbQba+Ga2X29su/KITph/Hg5\nXSs4kiNv/xGX1DUED9/nlevpSXMhNnu0Y8lJAwwp9husRHoL7CJ91QirUf+kms9R\nNHUA5xqNAgMBAAECggEABfSCSrphOi64/Ebk6mP3/FcHJDUDgfF8ZYgp8DBadjnZ\n4zTZFyUD995CSad5Y6893qZUJdVoKtakxr0Jy2++z5L99S7wPJR+ANGHGFSMhFOV\nON1iRBtpOfIKRoJtQNhEctH9QdogEI2y+6bJS68YVsGLIno/F8PF/2PIT2uS7SNc\nSvEVGA8GT/BqQP5UPiSjEtLw6mtF0hPcmpVsMjGwH+v8PMHKGohHxCUb8QrnxrMj\nZncGzNkb5KLcNwKBrLQBiCvWJTkB69NeUuBaaJfRiyS1BMobe3xonxQNR6C0C8IH\nW1x8R1iO0GUVTQoSsmbnsgAoXTKr1Mf107t32RT0wQKBgQDw/jOHz2QsrIUghAyQ\nQQIF5M+wdGZfRZHOfWXIGv2DCc7dtrUIQhp+HPtPdTbhXFdGwBpypOq7Mt1SOeqH\nrnzUd7IhGNknFHdkB4A5s1OPvTmS91O+Rde0vI+1xz+qnopaRSTMXqc3Ng+3yLbn\nx/FcOXOX+BjVruUjsd0+vJ73bQKBgQDni9nJEVp0r6FIGZd6ubUcLOqC7duWnZDB\n9dfy10mFHbNevaiCnhgEqvltzn7B2d7gjtm+tE7te733GIUK075+yLPpfgCjTehI\nj48fkRQ8fOeklnm0fuVw8U7vegr5RWVpgrajuNcyrkjx2OtUkxpJdjqkMUCYM6X/\nvJvUUgkboQKBgQDQ9urB2W/4WMO61SV7tBLH/4ajb9sQw2dR0GQAJn8qL8gDchj5\nhzAnqIO1e2LR+Nroy0xjmmK7XbiRQwz9B6zQItX/Yudwvotj3ikuXzOW0LJqoDEq\nLK+E1XgbXCD1ljFLYucsmuqNsj/g0Zbf1fyQRnTYElWee9/OmrzIWI/S5QKBgFxX\nEYt2ODTAtfki+54d4XRTFVMRuLjgLZKskGpwIQnNRnNJ/6HXmoyCAucfqr10PcYg\nMgYzsiZTavbX+HbQ6u906wr7DRYTQ8dsOQ/Fs+RLi7W/rNmmoanhEjG+4hF283KY\nhm3UkT3M85o/f9pCsAEL/WbtnW0Va+YJObv621cBAoGAcObi0XZxuqVhsCwGTU7V\nu/uORsf1E0LuXeLzNiMBoO84UMhxc+mFO1nurV0RqZ6wAyOELsHJIpWoueSJTWRl\nqw0wQ6y6UTvagGgzC+88SD7jRhJaBrnjsa9IDO98qzfgw/Oxb17611HUiaW/aNUl\nrXOuHaX8vHWS6dCNuvm+7qc=\n-----END PRIVATE KEY-----\n",
    "client_email": "joyfulbot@redditbot-363109.iam.gserviceaccount.com",
    "client_id": "105153036553319946005",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/joyfulbot%40redditbot-363109.iam.gserviceaccount.com"
}


def empty_row():
    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {
            'requests': [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "ROWS",
                            "startIndex": 2,
                            "endIndex": 3
                        },
                        "inheritFromBefore": True
                    }
                },
            ]
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId='1TFMDminuI5bj7767d1HKSG3OY6l6HG0wiDki9XA8TUU',
            body=body).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def worksheet_update(title, description, subreddit, dateTime, link):
    gc = gspread.service_account_from_dict(credens)
    sheets = gc.open_by_key('1TFMDminuI5bj7767d1HKSG3OY6l6HG0wiDki9XA8TUU')
    worksheet = sheets.sheet1
    worksheet.update('B3:F3', [[title, description, subreddit, dateTime, link]])


def sheets_batch_update():
    try:

        check_words = ['sadhguru', 'sad guru', 'jaggi', 'ishafoundation', 'isha', 'cult', 'god men', 'godmen']
        subreddit = reddit.subreddit("sadhguru") #1

        gc = gspread.service_account_from_dict(credens)
        sheets = gc.open_by_key('1TFMDminuI5bj7767d1HKSG3OY6l6HG0wiDki9XA8TUU')
        worksheet = sheets.sheet1

        for post in subreddit.new(limit=10):
            title_lower = post.title.lower()
            desc_lower = post.selftext.lower()
            checkTitle = False
            for x in check_words:
                if title_lower.__contains__(x) or desc_lower.__contains__(x):
                    checkTitle = True
                    post_title = str(post.title)
                    post_desc = str(post.selftext)
                    post_subreddit = str(post.subreddit)
                    postDateTime = str(datetime.fromtimestamp(post.created_utc))
                    postLink = str("www.reddit.com" + post.permalink)
                    empty_row()
                    worksheet_update(post_title, post_desc, post_subreddit, postDateTime, postLink)

            print("--------------------------")
            commentTitle = post.title
            post.comments.replace_more(limit=None)
            comment_queue = post.comments[:]
            if checkTitle == False:
                while comment_queue:
                    comment = comment_queue.pop(0)
                    comment_lower = comment.body.lower()
                    for x in check_words:
                        if comment_lower.__contains__(x):
                            commentDateTime = str(datetime.fromtimestamp(comment.created_utc))
                            commentBody = str(comment.body)
                            commentSubreddit = str(post.subreddit)
                            commentLink = str("www.reddit.com" + comment.permalink)
                            empty_row()
                            worksheet_update(commentTitle, commentBody, commentSubreddit, commentDateTime, commentLink)
                    comment_queue.extend(comment.replies)


    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    sheets_batch_update()
