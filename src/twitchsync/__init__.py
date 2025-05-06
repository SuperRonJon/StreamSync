import sys
import argparse
from .TwitchSync import TwitchSync
from .StreamsyncConfig import StreamsyncConfig

def main_cli():    
    parser = argparse.ArgumentParser(prog='twitchsync', description='Sync Twitch clips with other streamers', usage='twitchsync [--version] [-v] clip_url [streamers ...]')
    parser.add_argument('clip_url', nargs="?", default=None, help='Clip URL/Clip Slug/VOD Timestamp URL')
    parser.add_argument('streamers', nargs='*', default=None, help='Space separated list of streamers to get timestamps for')
    parser.add_argument('--version', action='version', version='%(prog)s v2.1.3')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Print details while running, mostly about discovering twitch credentials')
    parser.add_argument('--client_id', dest='client_id', default=None, metavar='TOKEN', help='Twitch application client id. Overrides finding from config file by default.')
    parser.add_argument('--client_secret', dest='client_secret', default=None, metavar='TOKEN', help='Twitch application client secret. Overrides finding from config file by default')
    parser.add_argument('--oauth_token', dest='oauth_token', default=None, metavar='TOKEN', help='Twitch application oauth token. Overrides finding from config file by default')
    parser.add_argument('-c', '--config', dest='custom_config_path', default=None, metavar='PATH', help='filepath to custom config file containing twitch client credentials.')
    args = parser.parse_args()

    quiet = not args.verbose
    twitchsync = TwitchSync(client_id = args.client_id, client_secret=args.client_secret, oauth_token=args.oauth_token, quiet=quiet, config_filepath=args.custom_config_path)

    if args.clip_url is None or args.streamers is None:
        stop = False
        print('Type "help" for help.\nType "exit" to quit.')
        while not stop:
            url = input('Enter clip slug or timestamped vod url: ')
            if url.lower() == 'exit':
                stop = True
                break
            if url.lower() == 'help':
                parser.print_help()
                continue
            users = input('Enter streamers: ')
            user_list = users.split()
            results = []
            try:
                results = twitchsync.get_matches_for_all_streamers(user_list, url)
            except Exception:
                print("Error reading clip.")
            for result in results:
                print(f"{result['streamer']}: {result['result']}")
            
    else:
        url = args.clip_url
        user_list = args.streamers
        if len(user_list) < 1:
            user_list = input('Enter streamers: ').split()
        results = []
        try:
            results = twitchsync.get_matches_for_all_streamers(user_list, url)
        except Exception:
            print("Error reading clip.")
        for result in results:
            print(f"{result['streamer']}: {result['result']}")
