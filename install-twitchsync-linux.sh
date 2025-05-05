#!/usr/bin/bash

mkdir -p $HOME/.config/twitchsync
python -m venv $HOME/.config/twitchsync/env
$HOME/.config/twitchsync/env/bin/pip install twitchsync
echo "The script may ask for your password to install the twitchsync command to your path so it can be ran directly\nIf you refuse you can still run it with 'python -m twitchsync'"
sudo ln -s $HOME/.config/twitchsync/env/bin/twitchsync /usr/local/bin/twitchsync
echo "Finished! Run 'twitchsync --help' to get started."
