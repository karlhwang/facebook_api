# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import config
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adaccount import AdAccount
import json
import sys
import pandas as pd
import requests
import datetime

def slack_alarm_fb_info(fb_info, ACCESS_TOKEN, channel_id):
    message = fb_info.to_string()
    data = {'Content-Type': 'application/x-www-form-urlencoded',
            'token': ACCESS_TOKEN,
            'channel': channel_id, 
            'text': message
            } 
    try:
        URL = "https://slack.com/api/chat.postMessage"
        res = requests.post(URL, data=data)
    except:
        print(3)

def get_date_range():
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=6)
    today = today.strftime('%Y-%m-%d')
    seven_days_ago = seven_days_ago.strftime('%Y-%m-%d')
    return seven_days_ago, today

if __name__ == "__main__":
    # Replace this with the place you installed facebookads using pip
    sys.path.append('/usr/local/lib/python3.9/site-packages/site-packages')
    # same as above
    sys.path.append(
        '/usr/local/lib/python3.9/site-packages/facebook_business-3.0.0-py2.7.egg-info')

    fb_access_token = config.FACEBOOK_ACCESS_TOKEN
    fb_ad_account_id = config.FACEBOOK_AD_ACCOUNT_ID
    fb_app_secret = config.FACEBOOK_APP_SECRET
    fb_app_id = config.FACEBOOK_APP_ID

    slack_access_token = config.SLACK_ACCESS_TOKEN
    slack_channel_id = config.SLACK_CHANNEL_ID

    FacebookAdsApi.init(access_token=fb_access_token)

    seven_days_ago, today = get_date_range()
    fields = [
        'campaign_name',
        'clicks',
        'spend',
    ]
    params = {
        'time_range': {'since': seven_days_ago, 'until': today},
        # 'level': 'adset',
        'level': 'campaign'
    }

    results =  AdAccount(fb_ad_account_id).get_insights(
        fields=fields,
        params=params,
    )
  
    df = pd.DataFrame(columns=['campaing_name', 'clicks','spend','date_start','date_stop'])
    contents_list = []
    for result in results:
        for key, value in result.items():
            contents_list.append(value)
        tmp_series = pd.Series(contents_list, index=df.columns)
        df = df.append(tmp_series, ignore_index=True)
        contents_list = []
    fb_info = df
    slack_alarm_fb_info(fb_info, slack_access_token, slack_channel_id)