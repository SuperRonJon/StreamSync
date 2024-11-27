import requests


class TwitchClient:
    def __init__(self, client_id, oauth_token):
        self.client_id = client_id
        self.oauth_token = oauth_token
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": "Bearer {}".format(self.oauth_token)
        }

    def get_clip(self, clip_slug):
        url = "https://api.twitch.tv/helix/clips?id={}".format(clip_slug)
        request = requests.get(url, headers=self.headers)
        if len(request.json()['data']) > 0:
            return request.json()['data'][0]
        else:
            return None

    def get_video(self, video_id):
        url = "https://api.twitch.tv/helix/videos/?id={}".format(video_id)
        request = requests.get(url, headers=self.headers)
        if len(request.json()['data']) > 0:
            return request.json()['data'][0]
        else: 
            return None

    def get_user_id(self, username):
        url = "https://api.twitch.tv/helix/users?login={}".format(username)
        request = requests.get(url, headers=self.headers)
        response = request.json()
        if len(response['data']) > 0:
            return response['data'][0]['id']
        else:
            return None

    def get_user_vods(self, username, limit=50):
        user_id = self.get_user_id(username)
        if user_id:
            url = "https://api.twitch.tv/helix/videos?user_id={}&first={}".format(user_id, limit)
            request = requests.get(url, headers=self.headers)
            response = request.json()
            return response['data']
        else:
            return None

