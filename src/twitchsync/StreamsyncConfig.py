import configparser
import os
import sys


class StreamsyncConfig:
    def __init__(self, config_filepath=None):
        self.none = 'NONE'
        self.config_filepath = None
        self.config_directory = None
        self.client_id = None
        self.oauth_token = None
        self.client_secret = None

        if config_filepath is not None:
            self.config_filepath = config_filepath
            self.config_directory = os.path.dirname(self.config_filepath)
        else:
            self.config_directory = self.get_default_config_dir()
            self.config_filepath = f"{self.config_directory}/streamsync.conf"
    
    def get_tokens_from_env(self):
        if 'TWITCHSYNC_TOKEN' in os.environ:
            self.oauth_token = os.environ['TWITCHSYNC_TOKEN']
        try:
            self.client_id = os.environ['TWITCHSYNC_ID']
            self.client_secret = os.environ['TWITCHSYNC_SECRET']
        except KeyError:
            return False
        return True

    def get_tokens_from_file(self):
        if not os.path.exists(self.config_filepath):
            return False
        config = configparser.ConfigParser()
        try:
            config.read(self.config_filepath)
            twitch_auth = config['TWITCH-AUTH']
            self.client_id = None if twitch_auth['CLIENT_ID'] == 'NONE' else twitch_auth['CLIENT_ID']
            self.client_secret = None if twitch_auth['CLIENT_SECRET'] == 'NONE' else twitch_auth['CLIENT_SECRET']
            if self.client_id is None or self.client_secret is None:
                return False
        except:
            return False
        if 'OAUTH_TOKEN' in twitch_auth:
            self.oauth_token = None if twitch_auth['OAUTH_TOKEN'] == 'NONE' else twitch_auth['OAUTH_TOKEN']
        return True
    
    def get_tokens_from_input(self):
        self.client_id = input("Enter client id: ")
        if self.client_id.lower() == "exit":
            sys.exit()
        self.client_secret = input("Enter client secret: ")
        if self.client_secret.lower() == "exit":
            sys.exit()
        input_token = input("Enter oauth token if you have one, otherwise leave blank: ")
        if input_token and not input_token.isspace():
            self.oauth_token = input_token

        if not self.client_id or not self.client_secret:
            return False
        elif self.client_id.isspace() or self.client_secret.isspace():
            return False
        else:
            return True

    def export_config_file(self):
        config = configparser.ConfigParser()
        _client_id = self.client_id if self.client_id is not None else self.none
        _client_secret = self.client_secret if self.client_secret is not None else self.none
        _oauth_token = self.oauth_token if self.oauth_token is not None else self.none
        config['TWITCH-AUTH'] = {
            'CLIENT_ID': _client_id,
            'CLIENT_SECRET': _client_secret,
            'OAUTH_TOKEN': _oauth_token
        }
        if self.config_directory is not None and not os.path.isdir(self.config_directory):
            os.makedirs(self.config_directory)
        if self.config_filepath is not None:
            with open (self.config_filepath, 'w') as f:
                config.write(f)
    
    def has_required_tokens(self):
        return self.client_id is not None and self.client_secret is not None
    
    def set_tokens(self, quiet=False):
        if not self.get_tokens_from_file():
            if not self.get_tokens_from_env():
                print("No tokens found...\n" \
                    "Set environment variables:\n\t" \
                    "TWITCHSYNC_ID with your client id\n\t" \
                    "TWITCHSYNC_SECRET with your client secret\n\t" \
                    "TWITCHSYNC_TOKEN with your oauth token, if you have one. If not one will be generated for you.\n" \
                    "Or enter your tokens below, enter exit to abort.")
                if not self.get_tokens_from_input():
                    print("Failed to get tokens...")
                    sys.exit()
                else:
                    print(f"Creating config file with given token at {self.config_filepath}...")
                    self.export_config_file()
            else:
                if not quiet:
                    print(f"Found tokens in environment, creating config file at {self.config_filepath}...")
                self.export_config_file()
        else:
            if not quiet:
                print(f"Found tokens in config file at {self.config_filepath}")
        
        if self.client_id is None or self.client_secret is None:
            print("Error, missing client id or client secret, both are required.")
            sys.exit()
        if self.oauth_token is None:
            from twitchsync.TwitchClient import refresh_token
            if not quiet:
                print(f"No oauth token found, generating a new one...")
            new_token = refresh_token(self.client_id, self.client_secret)
            if new_token is not None:
                if not quiet:
                    print(f"Received new token {new_token} - Updating config file...")
                self.oauth_token = new_token
                self.export_config_file()
            else:
                print("Error getting new token...")
                sys.exit()


    @staticmethod
    def get_default_config_dir():
        if 'PROGRAMDATA' in os.environ:
            return f"{os.environ['PROGRAMDATA']}/streamsync"
        elif 'HOME' in os.environ:
            return f"{os.environ['HOME']}/.config/streamsync"
        else:
            from pathlib import Path
            return f"{str(Path.home())}/.config/streamsync"
            