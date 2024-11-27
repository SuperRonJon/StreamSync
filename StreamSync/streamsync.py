from dateutil import parser
from .TwitchClient import TwitchClient
from secret import client_id as id, oauth_token as oauth
from isodate import parse_duration

import datetime
import re


client = TwitchClient(id, oauth)


# Returns the real-world time a moment in a video occurred at
# @param video_id: id of the video to be searched
# @param offset: the number of seconds into the video that the clip occured at
def get_time_from_offset(video_id, offset):
    vod = client.get_video(video_id)
    if vod is not None:
        vod_creation = parser.parse(vod['created_at'])
        return vod_creation + datetime.timedelta(seconds=offset)
    return None


# Returns the real-world time that the clip occurred at, or None if clip is not found
# @param clip_slug: twitch clip slug string
def get_time_from_clip(clip_string):
    clip_slug = None
    if clip_string.startswith("https://clips.twitch.tv/"):
        clip_slug = re.search(r"clips\.twitch\.tv\/(.*)", clip_string).group(1)
    elif clip_string.startswith("https://www.twitch.tv/"):
        clip_slug = re.search(r"\/clip\/([^?]*)", clip_string).group(1)
    else:
        clip_slug = clip_string
    clip = client.get_clip(clip_slug)
    if clip is not None and clip['video_id']:
        offset = clip['vod_offset']
        video_id = clip['video_id']
        return get_time_from_offset(video_id, offset)
    return None


# Returns the real-world time that a timestamped vod url occurred at, or None if no timestamp is found
# @param vod_url: twitch timestamped vod url string
def get_time_from_url(vod_url):
    t = re.search(r"\?t=(.*)|&t=(.*)", vod_url)
    v = re.search(r"videos\/(\d+)", vod_url)
    if t is not None and v is not None:
        timestamp = t.group(1) if t.group(1) else t.group(2)
        offset = parse_duration("PT" + timestamp.upper()).seconds
        video_id = v.group(1)
        return get_time_from_offset(video_id, offset)  
    return None


# Returns the real-world time of a vod or clip slug, or None if no proper clip or url is found
# @param url: clip slug or twitch timestamped vod url string
def get_time_from_input(url):
    url_time = get_time_from_url(url)
    if url_time is not None:
        return url_time
    clip_time = get_time_from_clip(url)
    return clip_time



# Returns the timestamped URL for specified streamer at the given time
# @param streamer: the username of the streamer desired
# @param clip_time: the real-world time that the timestamp should occur at
# @return None: Returns none if the channel was unable to be found
# @return Returns empty string if the vod for that time-period does not exist
def get_timestamp_for_streamer(streamer, clip_time):
    streamer_vods = client.get_user_vods(streamer)
    if streamer_vods is None:
        return f"Channel {streamer} not found."
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
        return "No vod found"

def get_matches_for_all_streamers(streamer_list, clip_string):
    clip_time = get_time_from_input(clip_string)
    results = []
    for streamer in streamer_list:
        match = get_timestamp_for_streamer(streamer, clip_time)
        current_result = {
            "streamer": streamer,
            "result": match 
        }
        results.append(current_result)
    return results
