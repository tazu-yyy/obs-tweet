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
autostart = None
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
    obs.obs_properties_add_bool(props, "autostart", "配信開始時に自動実行")
    obs.obs_properties_add_button(props, "button", "ツイート開始", start_button_callback)
    return props

def start_button_callback(props, prop):
    start_tweet()

def script_update(settings):
    global consumer_key, consumer_secret, access_token, access_token_secret, title, url, autostart
    title = obs.obs_data_get_string(settings, "title")
    url = obs.obs_data_get_string(settings, "url")
    consumer_key = obs.obs_data_get_string(settings, "consumer_key")
    consumer_secret = obs.obs_data_get_string(settings, "consumer_secret")
    access_token = obs.obs_data_get_string(settings, "access_token")
    access_token_secret = obs.obs_data_get_string(settings, "access_token_secret")
    autostart = obs.obs_data_get_bool(settings, "autostart")

def script_description():
    return "配信のーと: 自動ツイートは配信終了時、またはOBS終了時に自動停止します"

def update_client():
    global consumer_key, consumer_secret, access_token, access_token_secret, twitter_client

    if consumer_key and consumer_secret and access_token and access_token_secret:
        twitter_client = tweepy.Client(consumer_key=consumer_key,
                                       consumer_secret=consumer_secret,
                                       access_token=access_token,
                                       access_token_secret=access_token_secret)
        return True
    else:
        return False

def script_load(settings):
    obs.obs_frontend_add_event_callback(handle_event)

def script_unload():
    stop_tweet()

def handle_event(event):
    global tweet_counter, autostart

    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED and autostart:
        print("start streaming")
        start_tweet()
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        print("finish streaming")
        stop_tweet()

def start_tweet():
    tweet_counter = 0
    tweet_callback()
    obs.timer_add(tweet_callback, TWEET_INTERVAL)

def stop_tweet():
    obs.timer_remove(tweet_callback)

def tweet_callback():
    global tweet_counter, twitter_client, url, title
    print(f'{datetime.datetime.now().strftime("%m/%d %H:%M:%S")}')
    if not update_client():
        print("入力項目が足りません")
        return

    if tweet_counter == 0:
        text = f'【配信開始】{title} {url} #配信のーと {datetime.datetime.now().strftime("%m/%d %H:%M")}'
        print(f'Tweet: {text}')
        twitter_client.create_tweet(text=text)
    else:
        text = f'【{tweet_counter}時間経過】{title} {url} #配信のーと {datetime.datetime.now().strftime("%m/%d %H:%M")}'
        print(f'Tweet: {text}')
        twitter_client.create_tweet(text=text)
    tweet_counter += 1
