from django.shortcuts import render, HttpResponse
from reflections.models import Reflection
from reflections.models import Subject
from reflections.forms import ReflectionForm
from django.forms import modelformset_factory
from reflections.models import models
from dateutil import parser

try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

hashTags = ['#DataStructuresInRealLife', '#CompOrgInRealLife'];
hashTagDict = {}
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '963141792370749441-EvzYveF3rcNMSKLctuVPXX6eyzf3w45'
ACCESS_SECRET = 'DYGFBHsgaQtKfCHky8ka6ycZxsvLGSoDtuA0iUnIDSGQT'
CONSUMER_KEY = 'SC79UgCrSSxeV9mRDCvpfwBV2'
CONSUMER_SECRET = 'vFvQ09eQ1LprniqXOqUBKCmZgjKbMo7nzsjyZFegebVFkjpqjt'

def show_expert_view(request):
    get_tweets()
    reflection_form_set = modelformset_factory(Reflection, form=ReflectionForm, exclude=(), extra=0)
    form_set = reflection_form_set(queryset=Reflection.objects.filter(is_pending=True))
    # form_set = form_chunks(form_set.forms, 2)
    return render(request, 'expert/expert_page.html', {'reflection_form_set': form_set})


def submit_analysis(request):
    reflection_form_set = modelformset_factory(Reflection, form=ReflectionForm, exclude=(), extra=0)
    formset = reflection_form_set(request.POST, queryset=Reflection.objects.filter(is_pending=True))

    for reflection_form in formset:
        if reflection_form.is_valid() and reflection_form.has_changed():
            reflection = reflection_form.save(commit=False)
            reflection.is_pending = False
            reflection_form.save()

    return HttpResponse("Data Submitted Succesfully")


def form_chunks(forms, size):
    return [forms[i:i + size] for i in range(0, len(forms), size)]


def get_tweets():
    try:
        f = open("tweetsPointer.txt","r");
        for lines in f:
            tag = lines.split(":")[0].strip();
            pointer = lines.split(":")[1].strip();
            if(pointer == ""):
                pointer = "0";
            hashTagDict[tag] = pointer;
        f.close();
    except:
        pass

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    for hashTag in hashTags:
        if not hashTag in hashTagDict:
            hashTagDict[hashTag] = "0"

        last_tweet_id = hashTagDict[hashTag];
        # print(hashTag)
        # print("first" + last_tweet_id)
        if hashTagDict[hashTag] == "0":
            for status in tweepy.Cursor(api.search, q=hashTag, lang='en').items(200):
                finedData = status._json;

                subject = Subject(name = hashTag);
                subject.save();
                print(hashTag + finedData['id_str']);
                reflection = Reflection(tweet_id=finedData['id_str'], tweet_date=parser.parse(finedData['created_at']), student_id=finedData['user']['id_str'],
                    student_handle=finedData['user']['screen_name'], description=finedData['text'], subject=subject);
                reflection.save()
                if(finedData['id_str'] > last_tweet_id):
                    last_tweet_id = finedData['id_str'];
        else:
            for status in tweepy.Cursor(api.search, since_id=hashTagDict[hashTag], q=hashTag, lang='en').items(200):
                finedData = status._json;
                print(hashTag + finedData['id_str']);
                subject = Subject(name = hashTag);
                subject.save();

                reflection = Reflection(tweet_id=finedData['id_str'], tweet_date=parser.parse(finedData['created_at']), student_id=finedData['user']['id_str'],
                    student_handle=finedData['user']['screen_name'], description=finedData['text'], subject=subject);
                reflection.save()
                if(finedData['id_str'] > last_tweet_id):
                    last_tweet_id = finedData['id_str'];

        hashTagDict[hashTag] = last_tweet_id;

        # break

    f = open("tweetsPointer.txt","w");
    for item in hashTagDict:
        f.write(item + ":" + hashTagDict[item] + "\n");
    f.close();

            
                # if not finedData['id_str'] in tweets_id_list:

                

                

                


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







