import discord
from discord.ext import commands
from gspread.exceptions import APIError

from DataProviders.JorachBotProvider import get_jorach
from schema.emoji import get_emoji_map
from sheets.client import *


class CreateRaidCommand(commands.Cog):
    """
    `CreateRaidCommand` is a class that allows a user to start a new raid
    """

    @commands.command(name="startraid", description="Starts a new raid with a given name on a given date")
    async def run_command(self, ctx, raid_name: str, raid_month: int, raid_date: int, raid_time: str):
        """
        Registers the user in the spreadsheet provided all info is correct. Otherwise, informs the user that this
        command failed due to their syntax.

        :param ctx: The context of invocation for the command that sheet was ran on.
        """
        # remove colons because it screws up some sheets calls, heh
        raid_title = "Raid - {} {}/{} @ {}".format(raid_name, raid_month, raid_date, raid_time).replace(":", "")
        safe_raid_name = raid_name.replace(" ", "-")
        channel_name = "{}-{}-{}".format(raid_title, raid_month, raid_date)
        try:
            worksheet = duplicate_sheet(raid_title)
        except APIError:
            worksheet = get_worksheet(raid_title)

        embed = discord.Embed()
        embed.color = discord.Color.green()
        embed.title = raid_title
        embed.description = "React with your class or spec to register for the raid! Raid times are in server time (PST/PDT)"
        embed.add_field(name="DPS", value=0)
        embed.add_field(name="Healer", value=0)
        embed.add_field(name="Tank", value=0)

        guild = ctx.message.guild
        categories = guild.categories
        category = None
        for c in categories:
            if c.name.lower() == "raids":
                category = c
        if category == None:
            category = await guild.create_category("Raids")

        safe_raid_name = raid_name.replace(" ", "-")
        channel_name = "{}-{}-{}".format(safe_raid_name, raid_month, raid_date)
        for c in category.channels:
            if c.name == channel_name:
                print("Already have a channel with this name, cancelling")
                return
        channel = await category.create_text_channel(channel_name)

        msg = await channel.send(embed=embed)
        for key in get_emoji_map().keys():
            await msg.add_reaction(key)
        return