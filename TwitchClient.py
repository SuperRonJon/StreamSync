import requests


class TwitchClient:
    def __init__(self, client_id, oauth_token):
        self.client_id = client_id
        self.oauth_token = oauth_token
        self.headers = {
            "Client-ID": self.client_id,
            "Accept": "application/vnd.twitchtv.v5+json",
            "Authorization": "Bearer {}".format(self.oauth_token)
        }

    def get_clip(self, clip_slug):
        url = "https://api.twitch.tv/kraken/clips/{}".format(clip_slug)
        request = requests.get(url, headers=self.headers)
        return request.json()

    def get_video(self, video_id):
        url = "https://api.twitch.tv/kraken/videos/{}".format(video_id)
        request = requests.get(url, headers=self.headers)
        return request.json()

    def get_user_id(self, username):
        url = "https://api.twitch.tv/kraken/users?login={}".format(username)
        request = requests.get(url, headers=self.headers)
        response = request.json()
        if response['_total'] > 0:
            return response['users'][0]['_id']
        else:
            return None

    def get_user_vods(self, username, limit=50):
        user_id = self.get_user_id(username)
        if user_id:
            url = "https://api.twitch.tv/kraken/channels/{}/videos?limit={}&broadcast_type=archive".format(user_id, limit)
            request = requests.get(url, headers=self.headers)
            response = request.json()
            return response['videos']
        else:
            return None

