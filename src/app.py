import os
from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)
twitchsync = None

@app.route('/')
def index():
    return redirect(url_for("sync"))

@app.route('/api/sync', methods = ['POST'])
def api_sync():
    data = request.get_json()
    clip_input = data['url']
    streamers = data['streamers']
    results = twitchsync.get_matches_for_all_streamers(streamers, clip_input)
    return jsonify(results)

@app.route('/sync', methods=['GET'])
def sync():
    try:
        clip_input = request.args['url']
        streamers = request.args['streamers'].split()
    except Exception as e:
        return render_template("search.html", has_results=False, original_input="", streamer_list="")
    results = twitchsync.get_matches_for_all_streamers(streamers, clip_input)
    return render_template('search.html', has_results=True, results=results, original_input=clip_input, streamer_list=request.args['streamers'])
    

def main():
    from twitchsync import TwitchSync
    global twitchsync
    if twitchsync is None:
        twitchsync = TwitchSync(quiet=False)


main()

if __name__ == '__main__':
    PORT = None
    try:
        PORT = os.environ['PORT']
    except KeyError:
        PORT = 8080
    app.run(host='0.0.0.0', port=PORT)