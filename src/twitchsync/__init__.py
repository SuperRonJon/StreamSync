import sys
import argparse
from .streamsync import get_matches_for_all_streamers, init_client
from .StreamsyncConfig import StreamsyncConfig

def main_cli():
    config = StreamsyncConfig()
    config.set_tokens(quiet=True)
    init_client(config)
    
    parser = argparse.ArgumentParser(prog='twitchsync', description='Sync Twitch clips with other streamers')
    parser.add_argument('clip_url', help='Clip URL/Clip Slug/VOD Timestamp URL')
    parser.add_argument('streamers', nargs='+', help='Space separated list of streamers to get timestamps for')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v2.1.2')

    if len(sys.argv) <= 1:
        stop = False
        print('Type "exit" to quit.')
        while not stop:
            url = input('Enter clip slug or timestamped vod url: ')
            if url.lower() == 'exit':
                stop = True
                break
            users = input('Enter streamers: ')
            user_list = users.split()
            results = []
            try:
                results = get_matches_for_all_streamers(user_list, url)
            except Exception:
                print("Error reading clip.")
            for result in results:
                print(f"{result['streamer']}: {result['result']}")
            
    else:
        args = parser.parse_args()

        url = args.clip_url
        user_list = args.streamers
        results = []
        try:
            results = get_matches_for_all_streamers(user_list, url)
        except Exception:
            print("Error reading clip.")
        for result in results:
            print(f"{result['streamer']}: {result['result']}")
