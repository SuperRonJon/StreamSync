from dateutil import parser
from TwitchClient import TwitchClient
from secrets import client_id as id, oauth_token as oauth

import datetime

client = TwitchClient(id, oauth)
clip = client.get_clip("KawaiiLivelySpindleMVGame")
offset = clip['vod']['offset']
op_vod = client.get_video(clip['vod']['id'])
print('op_vod: {}'.format(clip['vod']['id']))
vod_creation = parser.parse(op_vod['created_at'])
clip_time = vod_creation + datetime.timedelta(seconds=offset)

new_user = 'trainwreckstv'
new_user_vods = client.get_user_vods(new_user)

found_vod = None

for vod in new_user_vods:
    start_time = parser.parse(vod['created_at'])
    end_time = start_time + datetime.timedelta(seconds=vod['length'])
    if(start_time < clip_time and clip_time < end_time):
        found_vod = vod
        break
    if(clip_time > start_time):
        break

if found_vod:
    print('found vod')
    offset = (clip_time - parser.parse(found_vod['created_at'])).total_seconds()
    hours = int(offset / 3600)
    minutes = int((offset / 60) % 60)
    seconds = int(offset % 60)
    output_url = "https://www.twitch.tv/videos/{}?t={}h{}m{}s".format(found_vod['_id'][1:], hours, minutes, seconds)
    print(output_url)
    
