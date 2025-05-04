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

Requires a twitch developer application code. 

To get one log into the twitch developer console with your twitch account https://dev.twitch.tv/console Then regester a new application, with category Application Integration and Confidential client type. 

Then once it is created click Manage -> New Secret and generate a new secret. Save this secret and the Client ID in a text file somewhere you will find them. Redirect url is not relevant, you can fill it out to your website, or this github page, etc.

The program will ask for these 2 tokens on the first run.

Now the program can be run with:

`python -m twitchsync clip_url/slug/vod_timestamp_url streamer1 streamer2 streamer3`

### Setting environment variables

This section is optional to have credentials be auto-detected on first run rather than manually enter them in the CLI.


(On Windows: Search->"Edit Environment Variables For Your Account"->New...)

(On Mac/Linux run `export TWITCHSYNC_ID=your client id && export TWITCHSYNC_SECRET=your client secret`)

TWITCHSYNC_ID=your client id

TWITCHSYNC_SECRET=your client secret

The environment variables do not need to be persistent, the credentials will be saved automatically and managed as necessary from now on.

Now it can be run like this `python -m twitchsync clip_url/slug/vod_timestamp streamer1 streamer2 streamer3`
