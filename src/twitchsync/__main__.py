import sys
import twitchsync

if __name__ == "__main__":
    from twitchsync.StreamsyncConfig import StreamsyncConfig
    config = StreamsyncConfig()
    config.set_tokens(quiet=True)
    twitchsync.init_client(config)
    if len(sys.argv) <= 1:
        stop = False
        print('Type "exit" to quit.')
        while not stop:
            url = input("Enter clip slug or timestamped vod url: ")
            if url.lower() == 'exit':
                stop = True
                break
            users = input('Enter streamers: ')
            user_list = users.split()
            results = []
            try:
                results = twitchsync.get_matches_for_all_streamers(user_list, url)
            except Exception:
                print("Error reading clip.")
            for result in results:
                print(f"{result['streamer']}: {result['result']}")
            
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        user_list = sys.argv[2:]
        results = []
        try:
            results = twitchsync.get_matches_for_all_streamers(user_list, url)
        except Exception:
            print("Error reading clip.")
        for result in results:
            print(f"{result['streamer']}: {result['result']}")
