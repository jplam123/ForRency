import datetime
import os

import tweepy as tweepy
from dotenv import load_dotenv
import pandas as pd
import senti_anal


def output_csv(data, hashtag, page_num):
    if page_num % 100 == 0:
        date_label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        df = pd.DataFrame(data)
        senti_anal.textblob_anal(df)
        print("....... outputting to csv", page_num, len(data))
        df.to_csv(f"{hashtag}_{page_num}_{date_label}.csv", index=False)
        print("  ..... resetting df")
        data = []
    return data


def mine_data(data, page):
    for tweet in page:
        mined = {
            "tweet_id": tweet.id,
            "name": tweet.user.name,
            "retweet_count": tweet.retweet_count,
            "text": tweet.full_text,
            "created_at": tweet.created_at,
            "hashtags": tweet.entities["hashtags"],
            "status_count": tweet.user.statuses_count,
            "followers_count": tweet.user.followers_count,
            "location": tweet.place,
        }

        try:
            mined["retweet_text"] = tweet.retweeted_status.full_text
        except:
            mined["retweet_text"] = "No RT Text"
        data.append(mined)


class TweetScraper:
    # Constants
    # API RELATED CONSTANTS
    load_dotenv()
    API_KEY = os.environ['API_KEY']
    API_SECRET_KEY = os.environ.get('API_SECRET_KEY')

    # API authentication for tweepy
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Defining the search terms as variables
    BTC_search_words = ["BTC", "bitcoin", "Bitcoin", "btc"]

    def hashtag_looper(self):
        for btc_word in self.BTC_search_words:
            self.hashtag_scraper(self, btc_word)

    def hashtag_scraper(self, hashtag: str):

        last_tweet_id = False
        page_num = 1

        data = []
        query = f"#{hashtag}"
        print(" ===== ", query)
        for page in tweepy.Cursor(
                self.api.search,
                q=query,
                lang="en",
                tweet_mode="extended",
                count=200,
        ).pages(400):
            print(f"page: {page_num}")
            page_num += 1

            mine_data(data, page)

            data = output_csv(data, hashtag, page_num)

        date_label = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        df = pd.DataFrame(data)
        senti_anal.textblob_anal(df)
        df.to_csv(f"{hashtag}_{page_num/100}_{date_label}.csv", index=False)


if __name__ == '__main__':
    t = TweetScraper
    t.hashtag_looper(t)
