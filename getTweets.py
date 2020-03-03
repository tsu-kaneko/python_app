# -*- coding: utf-8 -*-
import datetime
import json, config  # 標準のjsonモジュールとconfig.pyの読み込み
import re
import slackweb
from requests_oauthlib import OAuth1Session  # OAuthのライブラリの読み込み

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)  # 認証処理

url = "https://api.twitter.com/1.1/search/tweets.json"
params = {'q': '小田急線', 'count': 5, 'result_type': 'mixed', 'since': datetime.datetime.now()}
req = twitter.get(url, params=params)

# 通知内容
notifyContent = ''

# 遅延ツイートを取得・設定
if req.status_code == 200:
    res = json.loads(req.text)
    for line in res['statuses']:
        text = line['text']
        # if re.search('小田急', 'r' + text):
        if re.search('遅延|混雑|見合わせ', 'r' + text):
            print('*******************************************')
            print(text)
            notifyContent += "**************************************************************************\n"\
                             + text + "\n"
else:
    print("Failed: %d" % req.status_code)
    notifyContent = "Failed: %d" % req.status_code

# 空だったら通常運転
if len(notifyContent) == 0:
    notifyContent += 'おはようございます。本日の小田急線は通常運転です。'

# slackに通知
slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
slack.notify(text=notifyContent)
