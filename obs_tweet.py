import obspython as obs
import tweepy
import datetime

TWEET_INTERVAL = 1000 * 60 * 60

title = ""
url = ""
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
twitter_client = None
tweet_counter = 0

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "title", "タイトル", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "url", "宣伝URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "consumer_key", "API Key", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "consumer_secret", "API Secret", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "access_token", "Access Token", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "access_token_secret", "Access Token Secret", obs.OBS_TEXT_DEFAULT)
    return props

def script_update(settings):
    global consumer_key, consumer_secret, access_token, access_token_secret, title, url
    title = obs.obs_data_get_string(settings, "title")
    url = obs.obs_data_get_string(settings, "url")
    consumer_key = obs.obs_data_get_string(settings, "consumer_key")
    consumer_secret = obs.obs_data_get_string(settings, "consumer_secret")
    access_token = obs.obs_data_get_string(settings, "access_token")
    access_token_secret = obs.obs_data_get_string(settings, "access_token_secret")

def script_description():
    return "配信のーと"

def update_client():
    global consumer_key, consumer_secret, access_token, access_token_secret, twitter_client
    twitter_client = tweepy.Client(consumer_key=consumer_key,
                                   consumer_secret=consumer_secret,
                                   access_token=access_token,
                                   access_token_secret=access_token_secret)

def script_load(settings):
    obs.obs_frontend_add_event_callback(handle_event)

def script_unload():
    obs.timer_remove(tweet_callback)

def handle_event(event):
    global tweet_counter

    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        print("start streaming")
        tweet_counter = 0
        tweet_callback()
        obs.timer_add(tweet_callback, TWEET_INTERVAL)
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        print("finish streaming")
        obs.timer_remove(tweet_callback)

def tweet_callback():
    global tweet_counter, twitter_client, url, title
    print(f'{datetime.datetime.now().strftime("%m/%d %H:%M:%S")}')
    update_client()
    if tweet_counter == 0:
        text = f'【配信開始】{title} {url} #配信のーと {datetime.datetime.now().strftime("%m/%d %H:%M")}'
        print(f'Tweet: {text}')
        twitter_client.create_tweet(text=text)
    else:
        text = f'【{tweet_counter}時間経過】{title} {url} #配信のーと {datetime.datetime.now().strftime("%m/%d %H:%M")}'
        print(f'Tweet: {text}')
        twitter_client.create_tweet(text=text)
    tweet_counter += 1
