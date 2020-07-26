import os
import mysql.connector
import discord
from dotenv import load_dotenv
from discord.ext import commands
from mysql.connector import Error
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
config ={
	'user': os.getenv('MYSQL_USER'),
	'password': os.getenv('MYSQL_PASS'),
	'host': os.getenv('MYSQL_HOST'),
	'database': os.getenv('MYSQL_DB'),
	'raise_on_warnings': True

}

bot = commands.Bot(command_prefix='!')
bot.load_extension('membercommands')
bot.load_extension('knowledgebase')
welcomemsg = 'Welcome to Exoplanet - FC Modding! <:jackhat:528240349668179988>\n\nPlease take your time and read <#527327177285304350>!\n\nIf you want to learn more about how the server is structured have a look at <#527952199163183114>.\n\nIf you need any additional help feel free to message me with !help to display available commands.'

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
	await member.send(welcomemsg)

############  Command not found error handling  #############
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.author.send('Command not found!\n Use !help to display available commands.')
		channel_type = str(ctx.channel.type)			
		if channel_type != 'private':
			await ctx.message.delete()

bot.run(TOKEN)
