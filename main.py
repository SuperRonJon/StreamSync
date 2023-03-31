from dateutil import parser
from TwitchClient import TwitchClient
from secret import client_id as id, oauth_token as oauth
from isodate import parse_duration

import datetime


client = TwitchClient(id, oauth)


# Returns the real-world time that the clip occured at
# @param vod: vod json data as returned from TwitchClient
# @param offset: the number of seconds into the vod that the clip occured at
def get_time_from_offset(vod, offset):
    vod_creation = parser.parse(vod['created_at'])
    return vod_creation + datetime.timedelta(seconds=offset)


# Returns the timestamped URL for specified streamer at the given time
# @param streamer: the username of the streamer desired
# @param clip_time: the real-world time that the timestamp should occur at
# @return None: Returns none if the channel was unable to be found
# @return Returns empty string if the vod for that time-period does not exist
def get_timestamp_for_streamer(streamer, clip_time):
    streamer_vods = client.get_user_vods(streamer)
    if streamer_vods is None:
        return None
    found_vod = None

    for vod in streamer_vods:
        start_time = parser.parse(vod['created_at'])
        vod_length = parse_duration("PT" + vod['duration'].upper()).seconds
        end_time = start_time + datetime.timedelta(seconds=vod_length)
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
        output_url = "https://www.twitch.tv/videos/{}?t={}h{}m{}s".format(found_vod['id'], hours, minutes, seconds)
        return output_url
    else:
        return ""


clip_slug = input("Enter clip slug: ")
clip = client.get_clip(clip_slug)
if clip is not None and clip['video_id']:
    offset = clip['vod_offset']
    op_vod = client.get_video(clip['video_id'])
    if op_vod is not None:
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
    else:
        print("Error getting vod clip is from")
    input("Press Enter to continue...")
else:
    print('Error reading clip. Try again in a bit. The vod may not be available')
    input("Press Enter to continue...")
    
