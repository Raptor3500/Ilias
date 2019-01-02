import discord
from discord.ext import commands

OK = 0x89f442
Error = 0xf44141

ownerID = '274298631517896704'
class manage():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def load(self, ctx, extension_name : str):
        """Loads an extension."""
        extension_name = extension_name.strip()
        if "cogs." not in extension_name:
            extension_name = "cogs." + extension_name # nico load Owner => nico load cogs.Owner
            if ctx.message.author.id in ownerID:
                try:
                    self.bot.load_extension(extension_name)
                    embed = discord.Embed(title=None, description=None, color=OK)
                    embed.add_field(name=extension_name, value="Cog loaded.")
                    await self.bot.say(embed=embed)
                except (AttributeError, ImportError) as e:
                    embedError = discord.Embed(title=None, description=None, color=Error)
                    embedError.add_field(name='Cog Error', value="```py\n{}: {}\n```".format(type(e).__name__, str(e)), inline=True)
                    await self.bot.say(embed=embedError)
                    return
            else:
                noperm = discord.Embed(title=None, description=None, color=Error)
                noperm.add_field(name='Error', value='Are you sure you have permission to load ' + extension_name, inline=True)
                await self.bot.say(embed=noperm)

    @commands.command(pass_context=True)
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        extension_name = extension_name.strip()
        if "cogs." not in extension_name:
            extension_name = "cogs." + extension_name # nico unload Owner => nico unload cogs.Owner
            if ctx.message.author.id in ownerID:
                if "manage" in extension_name:
                    embed = discord.Embed(title=None, description=None, color=Error)
                    embed.add_field(name='Error', value=extension_name + " can't be unloaded.", inline=False)
                    await self.bot.say(embed=embed) # This obviously stops cogs.Owner from being disabled.
                else:
                    self.bot.unload_extension(extension_name)
                    embed = discord.Embed(title=None, description=None, color=OK)
                    embed.add_field(name=extension_name, value="Cog unloaded.")
                    await self.bot.say(embed=embed)
            else:
                noperm = discord.Embed(title=None, description=None, color=Error)
                noperm.add_field(name='Error', value='Are you sure you have enough permission to unload ' + extension_name, inline=True)
                await self.bot.say(embed=noperm)

                                                   
                                                   
                                                   
def setup(bot):
    bot.add_cog(manage(bot))
