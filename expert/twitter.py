from reflections.models import Reflection, Subject
from dateutil import parser as DateParser

import tweepy
import json

hashTagDict = {
    '#DataStructuresInRealLife': 'Data Structures',
    '#CompOrgInRealLife': 'Computer Organization'
}

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '963141792370749441-EvzYveF3rcNMSKLctuVPXX6eyzf3w45'
ACCESS_SECRET = 'DYGFBHsgaQtKfCHky8ka6ycZxsvLGSoDtuA0iUnIDSGQT'
CONSUMER_KEY = 'SC79UgCrSSxeV9mRDCvpfwBV2'
CONSUMER_SECRET = 'vFvQ09eQ1LprniqXOqUBKCmZgjKbMo7nzsjyZFegebVFkjpqjt'

#Do not change this unless you know it
manuallyAdding = False;


class TwitterAPI:

    @staticmethod
    def get_tweets():
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        count = 0;

        if manuallyAdding:
            
            f = open("manualTweets.txt","r");

            for line in f:
                count = count + 1;
                # print(count);

                parsed_data = json.loads(line);
                subject_name = hashTagDict[parsed_data["subject"]]
                
                subject = Subject.objects.get(name=subject_name)
                
                description = parsed_data['full_text']        
                reflection = Reflection(tweet_id=parsed_data['id_str'],
                                        student_id=parsed_data['user']['id_str'],
                                        student_handle=parsed_data['user']['screen_name'],
                                        date=DateParser.parse(parsed_data['created_at']),
                                        description=description,
                                        subject=subject);
                try:
                    reflection.save()
                except:
                    print("Failed");
            f.close()
    
        else:
            for hashTag in hashTagDict:
                subject_name = hashTagDict[hashTag]
                subject = Subject.objects.get(name=subject_name)
                # print(subject.id)

                subject_reflections = Reflection.objects.filter(subject=subject, is_pending=True)
                # print(subject_reflections)

                if subject_reflections.__len__() > 0:
                    last_tweet_id = subject_reflections.latest(field_name='tweet_id')
                    tweets = tweepy.Cursor(api.search, since_id=last_tweet_id, tweet_mode="extended", q=hashTag, lang='en').items(200)
                    print(last_tweet_id)
                else:
                    print('Nothing found, downloading last 200')
                    tweets = tweepy.Cursor(api.search, q=hashTag, tweet_mode="extended", lang='en').items(200)
        

                for status in tweets:
                    parsed_data = status._json;

                    # print(status)

                    # print(hashTag + parsed_data['id_str']);
                    description = parsed_data['full_text']        #We need to clean it afterwards
                    reflection = Reflection(tweet_id=parsed_data['id_str'],
                                            student_id=parsed_data['user']['id_str'],
                                            student_handle=parsed_data['user']['screen_name'],
                                            date=DateParser.parse(parsed_data['created_at']),
                                            description=description,
                                            subject=subject);
                    try:
                        reflection.save()
                    except:
                        print("Failed");

# #sample json format of tweet
# {
#     "created_at": "Wed Feb 20 22:31:42 +0000 2019",
#     "id": 1098349504707903488,
#     "id_str": "1098349504707903488", retri
#     "text": "A queue can be used to represent the line to speak to an advisor. Queues work in a first-in-first-out manner, so th\u2026 https://t.co/6nMwAGii0V",
#     "truncated": true,
#     "entities": {
#         "hashtags": [],
#         "symbols": [],
#         "user_mentions": [],
#         "urls": [{
#             "url": "https://t.co/6nMwAGii0V",
#             "expanded_url": "https://twitter.com/i/web/status/1098349504707903488",
#             "display_url": "twitter.com/i/web/status/1\u2026",
#             "indices": [117, 140]
#        }]
#     },
#     "metadata": {
#         "iso_language_code": "en",
#         "result_type": "recent"
#     },
#     "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
#     "in_reply_to_status_id": null,
#     "in_reply_to_status_id_str": null,
#     "in_reply_to_user_id": null,
#     "in_reply_to_user_id_str": null,
#     "in_reply_to_screen_name": null,
#     "user": {
#         "id": 1098348490806185984,
#         "id_str": "1098348490806185984",
#         "name": "erin wilhjelm",
#         "screen_name": "WilhjelmErin",
#         "location": "",
#         "description": "",
#         "url": null,
#         "entities": {
#             "description": {
#                 "urls": []
#             }
#         },
#         "protected": false,
#         "followers_count": 0,
#         "friends_count": 0,
#         "listed_count": 0,
#         "created_at": "Wed Feb 20 22:27:41 +0000 2019",
#         "favourites_count": 0,
#         "utc_offset": null,
#         "time_zone": null,
#         "geo_enabled": false,
#         "verified": false,
#         "statuses_count": 1,
#         "lang": "en",
#         "contributors_enabled": false,
#         "is_translator": false,
#         "is_translation_enabled": false,
#         "profile_background_color": "F5F8FA",
#         "profile_background_image_url": null,
#         "profile_background_image_url_https": null,
#         "profile_background_tile": false,
#         "profile_image_url": "http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
#         "profile_image_url_https": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
#         "profile_link_color": "1DA1F2",
#         "profile_sidebar_border_color": "C0DEED",
#         "profile_sidebar_fill_color": "DDEEF6",
#         "profile_text_color": "333333",
#         "profile_use_background_image": true,
#         "has_extended_profile": false,
#         "default_profile": true,
#         "default_profile_image": true,
#         "following": false,
#         "follow_request_sent": false,
#         "notifications": false,
#         "translator_type": "none"
#     },
#     "geo": null,
#     "coordinates": null,
#     "place": null,
#     "contributors": null,
#     "is_quote_status": false,
#     "retweet_count": 0,
#     "favorite_count": 0,
#     "favorited": false,
#     "retweeted": false,
#     "lang": "en"
# }
