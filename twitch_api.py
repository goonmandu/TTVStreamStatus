import requests
from twitch_auth import *


def _api_endpoint_json(endpoint: str, client_id: str, access_token: str):
    response = requests.get(
        endpoint,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Client-Id": client_id,
        }
    )

    return response.json()


def is_username_live(username: str) -> bool:
    endpoint = f"https://api.twitch.tv/helix/streams?user_login={username}"
    stream = _api_endpoint_json(endpoint, CLIENT_ID, ACCESS_TOKEN)
    try:
        return bool(stream["data"])
    except KeyError:
        print("CRITICAL: Something went wrong:\n"
              "Cannot find key 'data' in response JSON.")
        return False


if __name__ == "__main__":
    streamer_username = "shroud"
    print(f"Is {streamer_username} live?")
    print(is_username_live(streamer_username))
