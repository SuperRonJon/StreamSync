import requests


def refresh_token(client_id, client_secret):
    url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
    request = requests.post(url)
    response = request.json()
    return response['access_token']


class TwitchClient:
    def __init__(self, streamsync_config):
        self.streamsync_config = streamsync_config
        self.client_id = streamsync_config.client_id
        self.client_secret = streamsync_config.client_secret
        self.oauth_token = streamsync_config.oauth_token
    
    def headers(self):
        return {
            "Client-ID": self.client_id,
            "Authorization": "Bearer {}".format(self.oauth_token)
        }
    
    def make_request(self, url):
        request = requests.get(url, headers=self.headers())
        if request.status_code == requests.codes.unauthorized:
            print("Invalid oauth token... Generating a new one...")
            self.oauth_token = refresh_token(self.client_id, self.client_secret)
            self.streamsync_config.oauth_token = self.oauth_token
            self.streamsync_config.export_config_file()
            print(f"Generated new oauth token {self.oauth_token} and re-trying request...")
            request = requests.get(url, headers=self.headers())
            if request.status_code != requests.codes.ok:
                print(f"Still unable to complete the request for some reason... Status code {str(request.status_code)}")
                return None
        
        return request

    def get_clip(self, clip_slug):
        url = "https://api.twitch.tv/helix/clips?id={}".format(clip_slug)
        request = self.make_request(url)
        if request is None:
            return None
        if len(request.json()['data']) > 0:
            return request.json()['data'][0]
        else:
            return None

    def get_video(self, video_id):
        url = "https://api.twitch.tv/helix/videos/?id={}".format(video_id)
        request = self.make_request(url)
        if request is None:
            return None
        if len(request.json()['data']) > 0:
            return request.json()['data'][0]
        else: 
            return None

    def get_user_id(self, username):
        url = "https://api.twitch.tv/helix/users?login={}".format(username)
        request = self.make_request(url)
        if request is None:
            return None
        response = request.json()
        if len(response['data']) > 0:
            return response['data'][0]['id']
        else:
            return None

    def get_user_vods(self, username, limit=50):
        user_id = self.get_user_id(username)
        if user_id:
            url = "https://api.twitch.tv/helix/videos?user_id={}&first={}".format(user_id, limit)
            request = self.make_request(url)
            if request is None:
                return None
            response = request.json()
            return response['data']
        else:
            return None

