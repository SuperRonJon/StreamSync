import os
import sys
import StreamSync
from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("sync"))

@app.route('/api/sync', methods = ['POST'])
def api_sync():
    data = request.get_json()
    clip_input = data['url']
    streamers = data['streamers']
    results = StreamSync.get_matches_for_all_streamers(streamers, clip_input)
    return jsonify(results)

@app.route('/sync', methods=['GET'])
def sync():
    try:
        clip_input = request.args['url']
        streamers = request.args['streamers'].split()
    except Exception as e:
        return render_template("search.html", has_results=False, original_input="", streamer_list="")
    results = StreamSync.get_matches_for_all_streamers(streamers, clip_input)
    return render_template('search.html', has_results=True, results=results, original_input=clip_input, streamer_list=request.args['streamers'])
    

def main():
    from StreamSync.StreamsyncConfig import StreamsyncConfig
    config = StreamsyncConfig()

    if not config.get_tokens_from_file():
        if not config.get_tokens_from_env():
            print("No tokens found...\n" \
            "Set environment variables:\n\t" \
            "STREAMSYNC_ID with your client id\n\t" \
            "STREAMSYNC_SECRET with your client secret\n\t" \
            "STREAMSYNC_TOKEN with your oauth token, if you have one. If not one will be generated for you.\n " \
            "Shutting down for now... Maybe in the future you can enter you tokens here :)")
            sys.exit()
        else:
            # Tokens found in env and not in file, new file should be created
            print(f"Found tokens in environment, creating config file at {config.config_filepath}...")
            config.export_config_file()

    if config.client_id is None or config.oauth_token is None:
        from StreamSync.TwitchClient import refresh_token
        print("Missing OAuth token, attempting to refresh...")
        token = refresh_token(config.client_id, config.client_secret)
        if token is not None:
            print(f"Received new token {token} - Updating config file...")
            config.oauth_token = token
            config.export_config_file()
        else:
            print("Error getting new token...")
            sys.exit()
    else:
        print(f"Found tokens in config file at {config.config_filepath}")

    StreamSync.init_client(config)


main()

if __name__ == '__main__':
    PORT = None
    try:
        PORT = os.environ['PORT']
    except KeyError:
        PORT = 8080
    app.run(host='0.0.0.0', port=PORT)