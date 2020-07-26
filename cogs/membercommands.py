import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
load_dotenv()

bot = commands.Bot(command_prefix='!')
class Roles(commands.Cog):

	def __init__(self, bot):
	        self.bot = bot

	async def role_swap(self, ctx, rolename):
		channel_type = str(ctx.channel.type)
		if channel_type != 'private':
			guild = ctx.message.guild.id
			exofc_modding = os.getenv('DISCORD_EXOMOD')
			if guild == exofc_modding:
				user = ctx.message.author
				role = get(user.guild.roles, name=rolename.lower())
				try:	
					if role in user.roles:
						await user.remove_roles(role)
						await ctx.author.send(rolename + ' role removed!')
						await ctx.message.delete()
					else:
						await user.add_roles(role)
						await ctx.author.send(rolename + ' role added!')
						await ctx.message.delete()
				except Exception as e:
					print(str(e))
					await ctx.message.delete()
			else:
				await ctx.author.send('This command can\'t be used on this server.')
				await ctx.message.delete()
		else:
			await ctx.author.send('This Command can\'t be used in a private Conversation.')

############  Role commands  #############
	@bot.command(name='modder', help='Grants or revokes modder role', pass_context=True)
	async def modderdm (self, ctx):
		await self.role_swap(ctx, 'Modder')
	@bot.command(name='de', help='Grants or revokes access to the german channels')
	async def dedm (self, ctx):
		await self.role_swap(ctx, 'DE')

	@bot.command(name='en', help='Grants or revokes access to the english channels')
	async def endm (self, ctx):
		await self.role_swap(ctx, 'EN')

	@bot.command(name='ru', help='Grants or revokes access to the russian channels')
	async def rudm (self, ctx):
		await self.role_swap(ctx, 'RU')

def setup(bot):
	bot.add_cog(Roles(bot))

