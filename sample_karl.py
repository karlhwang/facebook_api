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
# Replace this with the place you installed facebookads using pip
sys.path.append('/usr/local/lib/python3.9/site-packages/site-packages')
# same as above
sys.path.append(
    '/usr/local/lib/python3.9/site-packages/facebook_business-3.0.0-py2.7.egg-info')


access_token = config.access_token
ad_account_id = config.ad_account_id
app_secret = config.app_secret
app_id = config.app_id

FacebookAdsApi.init(access_token=access_token)

fields = [

    'clicks',
    'campaign_name',
    'spend'
]
params = {
    'time_range': {'since': '2021-07-20', 'until': '2021-07-20'},
    # 'level': 'adset',
    'level': 'campaign'

}


print(AdAccount(ad_account_id).get_insights(
    fields=fields,
    params=params,
))
