import os
from flask import Flask, jsonify, request, render_template
from main import get_matches_for_all_streamers

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("search.html", has_results=False)

@app.route('/api/sync', methods = ['POST'])
def api_sync():
    data = request.get_json()
    clip_input = data['url']
    streamers = data['streamers']
    results = get_matches_for_all_streamers(streamers, clip_input)
    return jsonify(results)

@app.route('/sync', methods=['GET'])
def sync():
    clip_input = request.args['url']
    streamers = request.args['streamers'].split()
    results = get_matches_for_all_streamers(streamers, clip_input)
    return render_template('search.html', has_results=True, results=results, original_input=clip_input)
    

if __name__ == '__main__':
    PORT = None
    try:
        PORT = os.environ['PORT']
    except KeyError:
        PORT = 8080
    app.run(host='0.0.0.0', port=PORT)