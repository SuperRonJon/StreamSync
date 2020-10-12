from dateutil import parser
from TwitchClient import TwitchClient
from secrets import client_id as id, oauth_token as oauth

import datetime


client = TwitchClient(id, oauth)


def get_time_from_offset(vod, offset):
    vod_creation = parser.parse(vod['created_at'])
    return vod_creation + datetime.timedelta(seconds=offset)


def get_timestamp_for_streamer(streamer, clip_time):
    streamer_vods = client.get_user_vods(streamer)
    if streamer_vods is None:
        return None
    found_vod = None

    for vod in streamer_vods:
        start_time = parser.parse(vod['created_at'])
        end_time = start_time + datetime.timedelta(seconds=vod['length'])
        if(start_time < clip_time and clip_time < end_time):
            found_vod = vod
            break
        if clip_time > start_time:
            break
    
    if found_vod:
        offset = (clip_time - parser.parse(found_vod['created_at'])).total_seconds()
        hours = int(offset / 3600)
        minutes = int((offset / 60) % 60)
        seconds = int(offset % 60)
        output_url = "https://www.twitch.tv/videos/{}?t={}h{}m{}s".format(found_vod['_id'][1:], hours, minutes, seconds)
        return output_url
    else:
        return ""


clip_slug = input("Enter clip slug: ")
clip = client.get_clip(clip_slug)
if not 'error' in clip and clip['vod'] is not None:
    offset = clip['vod']['offset']
    op_vod = client.get_video(clip['vod']['id'])
    clip_time = get_time_from_offset(op_vod, offset)

    new_users = input("Enter streamers: ")
    user_list = new_users.split()
    for user in user_list:
        output = get_timestamp_for_streamer(user, clip_time)
        if output is not None:
            if output:
                print("{}: {}".format(user, output))
            else:
                print("{}: No vod found".format(user))
        else:
            print("{}: Unable to find channel".format(user))
    input("Press Enter to continue...")
else:
    if 'message' in clip:
        print(clip['message'])
    else:
        print('Error reading clip. Try agian in a bit.')
    input("Press Enter to continue...")
    
