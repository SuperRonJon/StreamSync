# TwitchSync

Syncs twitch clips with other streamers. 

Input a twitch clip url, slug, or vod timestamp with a list of streamers, and the program will output a list of timestamped urls for the same moment in each streamer's vod.

```
$ python -m twitchsync https://www.twitch.tv/thebigmeech/clip/AgreeableNurturingFishPanicVis-g_-jghN2s5rElLpo sgtapollo lisajfc thebigmeech
sgtapollo: https://www.twitch.tv/videos/2448466929?t=2h20m44s
lisajfc: https://www.twitch.tv/videos/2448318187?t=6h0m38s
thebigmeech: https://www.twitch.tv/videos/2448294467?t=6h42m42s
```

Supported input formats:
- Clip URL: `https://www.twitch.tv/thebigmeech/clip/AgreeableNurturingFishPanicVis-g_-jghN2s5rElLpo`
- Clip slug: `AgreeableNurturingFishPanicVis-g_-jghN2s5rElLpo`
- Timestamped vod URL: `https://www.twitch.tv/videos/2448294467?t=6h42m42s`

## Installation
`pip install twitchsync`

For Mac & Linux there is an easy install script that will install the command to a private venv and symlink it onto your path for easy use. Requires python to be installed.

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/SuperRonJon/TwitchSync/master/install-twitchsync-linux.sh)"
```

## Requirements

Requires Python 3.9+

Requires a twitch developer application client id & secret pair. 

To get one log into the twitch developer console with your twitch account https://dev.twitch.tv/console Then regester a new application, with category Application Integration and Confidential client type. Redirect url is not relevant, you can fill it out to your website, or this github page, etc.

Then once it is created click Manage -> New Secret and generate a new secret. Save this secret and the Client ID in a text file somewhere you will find them.

The program will ask for these 2 tokens on the first run.

Now the program can be run with:

`python -m twitchsync clip_url/slug/vod_timestamp_url streamer1 streamer2 streamer3`

On the first run, the program will ask for your twitch application client credentials if it cannot find them. You can enter them here or by passing them as optional arguments on the first run like below.

`python -m twitchsync --client_id <token> --client_secret <token>`

Once you have set your tokens once the program will store them in a configuration file and you will not need to enter them again.

You can also set up your configuration by setting up environment variables, explained in the following section.

### Setting environment variables

This section is optional to have credentials be auto-detected on first run rather than manually enter them in the CLI.


(On Windows: Search->"Edit Environment Variables For Your Account"->New...)

(On Mac/Linux run `export TWITCHSYNC_ID=your client id && export TWITCHSYNC_SECRET=your client secret`)

TWITCHSYNC_ID=your client id

TWITCHSYNC_SECRET=your client secret

The environment variables do not need to be persistent, the credentials will be saved automatically and managed as necessary from now on.

Now it can be run like this `python -m twitchsync clip_url/slug/vod_timestamp streamer1 streamer2 streamer3`

# Importing as python module

Twitchsync can also be imported as a python module to be used in custom code. An example using credentials from the default config file, same as the instructions above:

```python
from twitchsync import TwitchSync

client = TwitchSync()
clip_url = "https://www.twitch.tv/clip/or/vod/timestamp"
streamer_list = ["streamer1", "streamer2", "streamer3"]

matches = client.get_matches_for_all_streamers(streamer_list, clip_url)
for match in matches:
  print(f"{match["streamer"]}: {match["result"]}")

single_match = client.get_match_for_streamer("streamer1", clip_url)
print(f"{single_match["streamer"]: single_match["result"]}")
```
