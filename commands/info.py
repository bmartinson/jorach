from discord.ext import commands

from schema.roles import get_all_roles
from sheets.client import *


class Info(commands.Cog):
    """
    `Info` is a class that contains a variety of info-providing commands.
    """

    @commands.command()
    async def roles(self, ctx):
        """
        Shows what roles are available.

        DEVELOPER INFO:
        :param ctx: The context of invocation for the command that sheet was ran on.
        :param params: No parameters are used.
        """
        await ctx.send("Valid roles are: %s" % ", ".join(get_all_roles()))
        return

    @commands.command()
    async def raids(self, ctx):
        """
        Shows what raids are available.

        DEVELOPER INFO:
        :param ctx: The context of invocation for the command that sheet was ran on.
        :param params: No parameters are used.
        """
        raid_names = [ws.title for ws in get_raid_worksheets()]

        if not raid_names:
            await ctx.send("There are no raids scheduled right now.")
        else:
            await ctx.send("Available raids are:\n - %s" % ("\n - ".join(raid_names)))
        return

    @commands.command()
    async def sheet(self, ctx):
        """
        Links the current raid signup sheet.

        DEVELOPER INFO:
        :param ctx: The context of invocation for the command that sheet was ran on.
        """
        await ctx.send("See the spreadsheet at:\n %s" % get_spreadsheet_link())
        return