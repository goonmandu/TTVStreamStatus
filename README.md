# TTVStreamStatus
This Bot changes a Discord Voice Channel's name to whatever you choose based on whether the specified Twitch streamer is online or offline.

## Requirements
- Python 3.8 or newer
- Python dependencies:
    ```shell
    pip3 install -r requirements.txt
    ```

## Usage
1. Create a Discord Bot, get the bot token, then invite the bot to your Discord server.
   - [Tutorial - discordpy.readthedocs.io](https://discordpy.readthedocs.io/en/stable/discord.html)
     - Only tick the `Manage Channels` checkbox under `Bot Permissions` in the OAuth2 tab.
2. Create a Twitch Application and get the following:
   - Client ID
   - Client Secret
   - Access Token
   - [Tutorial - dev.twitch.tv](https://dev.twitch.tv/docs/api/get-started/)
3. Create the following files in the same directory/folder as all other source code files:
   - `discord_auth.py`
   - `twitch_auth.py`
4. Fill in the following information in the respective files:
   - `discord_auth.py`
     ```python
     BOT_TOKEN = "The bot token"  # in quotes.
     ```
   - `twitch_auth.py`
     ```python
     CLIENT_ID = "The client ID"  # in quotes.
     CLIENT_SECRET = "The client secret"  # in quotes.
     ACCESS_TOKEN = "The access token"  # in quotes.
     ```
5. Run the bot.
    ```shell
    python3 main.py
    ```
6. With the bot online, you may want to specify the following:
   - The Discord Voice Channel ID
     - `ss!vc voice_channel_id`
   - The Twitch Streamer's username
     - `ss!ttv twitch_streamer_username`
   - The text to display when the Twitch Streamer is online
     - `ss!on online_text`
   - The text to display when the Twitch Streamer is offline
     - `ss!off offline_text`
7. These changes get saved in `bot_config.json` and are automatically loaded upon bot startup so that you don't have to enter them again if the bot shuts down.