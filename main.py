# File Structure     FROM -  TO
#
# IMPORTS              4  -   10
# CLASS DEFINITION    14  -   77
# BOT RUNTIME SETUP   82  -   84
# COMMANDS            88  -  116
# BOT.RUN()          121  -  124

import os
import json
import discord
from discord.ext import tasks, commands
from twitch_api import is_username_live
from discord_auth import BOT_TOKEN
import logging


class StreamStatus(commands.Bot):
    async def setup_hook(self) -> None:
        print("Starting initial setup")
        if os.path.exists("bot_config.json"):
            with open("bot_config.json", "r") as f:
                self.config = json.load(f)
        else:
            with open("bot_config.json", "w+") as f:
                json.dump(
                    {
                        "voice_channel_id": None,
                        "twitch_channel_name": None,
                        "online_message": "ONLINE",
                        "offline_message": "OFFLINE"
                    },
                    f,
                    indent=2
                )
                self.config = json.load(f)

        print("Initial setup done!")

    async def on_ready(self) -> None:
        self.voice_channel = self.get_channel(int(self.config["voice_channel_id"]))
        self.update_status_channel.start()
        print('Logged in!')

    # Process commands
    async def on_message(self, msg):
        if msg.author.bot:
            return
        await self.process_commands(msg)

    # Return True if live, False if not live
    async def get_streamer_status(self, twitch_id: str) -> bool:
        return is_username_live(twitch_id)

    # Channel name update logic
    # WARNING: Updating channels is rate-limited by Discord to 2 times per 10 minutes.
    # The interval specified "minutes=X" must respect the limit.
    @tasks.loop(minutes=6)
    async def update_status_channel(self):
        print("Updating status channel")
        if not (self.config["twitch_channel_name"] and self.voice_channel):
            print("Incorrect data for either ttv name or vc")
            print(f"{self.config['twitch_channel_name']}, {self.voice_channel}")
            return
        else:
            if isinstance(self.voice_channel, discord.VoiceChannel):
                print("Editing channel")
                live = await self.get_streamer_status(self.config["twitch_channel_name"])
                print(live)
                if live:
                    print("Streamer was live")
                    await self.voice_channel.edit(name=self.config["online_message"])
                else:
                    print("Streamer was offline")
                    await self.voice_channel.edit(name=self.config["offline_message"])
            else:
                print("self.vc wasnt an object of dc.VC")
                print(self.voice_channel)


# Bot permissions and setup
intents = discord.Intents.default()
intents.message_content = True
bot = StreamStatus(intents=intents, command_prefix="ss!")


# Setter commands
@bot.command()
@commands.has_permissions(administrator=True)
async def ttv(ctx, ttv_name):
    bot.config["twitch_channel_name"] = ttv_name
    await ctx.send(f"Twitch channel changed to `{bot.config['twitch_channel_name']}`!\n"
                   f"https://twitch.tv/{bot.config['twitch_channel_name']}")
    json.dump(bot.config, open("bot_config.json", "w"), indent=2)


@bot.command()
@commands.has_permissions(administrator=True)
async def vc(ctx, voice_channel_id):
    bot.config["voice_channel_id"] = voice_channel_id
    bot.voice_channel = bot.get_channel(int(bot.config["voice_channel_id"]))
    await ctx.send(f"Voice channel ID changed to `{bot.config['voice_channel_id']}`")
    json.dump(bot.config, open("bot_config.json", "w"), indent=2)


@bot.command()
@commands.has_permissions(administrator=True)
async def on(ctx, *online_message):
    bot.config["online_message"] = ' '.join(map(str, online_message))
    await ctx.send(f"Online message changed to `{bot.config['online_message']}`")
    json.dump(bot.config, open("bot_config.json", "w"), indent=2)


@bot.command()
@commands.has_permissions(administrator=True)
async def off(ctx, *offline_message):
    bot.config["offline_message"] = ' '.join(map(str, offline_message))
    await ctx.send(f"Offline message changed to `{bot.config['offline_message']}`")
    json.dump(bot.config, open("bot_config.json", "w"), indent=2)


# Run bot
if __name__ == "__main__":
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    bot.run(BOT_TOKEN, log_handler=handler, log_level=2)
