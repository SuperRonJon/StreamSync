import sys
from twitchsync import main_cli

if __name__ == "__main__":
    try:
        main_cli()
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting...")
        sys.exit(130)
