import mysql.connector
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from mysql.connector import Error
load_dotenv()
config ={
	'user': os.getenv('MYSQL_USER'),
	'password': os.getenv('MYSQL_PASS'),
	'host': os.getenv('MYSQL_HOST'),
	'database': os.getenv('MYSQL_DB'),
	'raise_on_warnings': True
}

bot = commands.Bot(command_prefix='!')

class Knowledgebase(commands.Cog):

	def __init__(self, bot):
	        self.bot = bot

	def connect(self):
		self.connection = mysql.connector.connect(**config)
		self.cursor = self.connection.cursor(buffered=True)

	def disconnect(self):
		self.cursor.close()
		self.connection.close()

	async def query_get_rows(self, ctx, tablename):
		embedVar = discord.Embed(title=tablename, description='', color=0xffffff)
		row_names=os.getenv(tablename.upper())
		self.cursor.execute('SELECT ' + row_names + ' FROM ' + tablename.lower())
		self.row = self.cursor.fetchone()
		while self.row is not None:
			embedVar.add_field(name=self.row[0], value=self.row[1] + '\n' + self.row[2], inline=False)
			self.row = self.cursor.fetchone()
		await ctx.author.send(embed=embedVar)
		channel_type = str(ctx.channel.type)			
		if channel_type != 'private':
			await ctx.message.delete()
	

	async def query_get_rows_where(self, ctx, tablename, whereclause):
		embedVar = discord.Embed(title='', description='', color=0xffffff)
		channel_type = str(ctx.channel.type)
		row_names=os.getenv(tablename.upper())
		try:
			self.cursor.execute('SELECT ' + row_names + ' FROM ' + tablename + ' WHERE ' + tablename + '_name = ' + whereclause)
			self.row = self.cursor.fetchone()
		except mysql.connector.Error as err:
			self.row = 'error'
		if self.row != 'error':
			while self.row is not None:
				embedVar.add_field(name=row[0], value=row[1], inline=False)
				self.row = self.cursor.fetchone()
			await ctx.author.send(embed=embedVar)
			if channel_type != 'private':
				await ctx.message.delete()
		else:
			await ctx.author.send('Nothing found!')
			if channel_type != 'private':
				await ctx.message.delete()
		
############  Knowledgebase commands  #############
	@bot.command(name='folder', help='Lists information about the provided folder. \nUsage: !folder foldername')
	async def folderdm (self, ctx, foldername):
		self.connect()
		await self.query_get_rows_where(ctx, 'folder', foldername)

	@bot.command(name='lua', help='Lists information about the provided lua file. \nUsage: !lua filename \n Extension .lua is not required!')
	async def luadm (self, ctx, luaname):
		self.connect()
		await self.query_get_rows_where(ctx, 'lua', luaname)

	@bot.command(name='function', help='Lists information about the provided function. \nUsage: !function functionname \n () or additional arguments are not required!')
	async def functiondm (self, ctx, functionname):	
		self.connect()
		await self.query_get_rows_where('function', functionname)

	@bot.command(name='tutorials', help='Displays a list of available tutorials about various topics')
	async def tutorialsdm (self, ctx):
		self.connect()
		await self.query_get_rows(ctx, 'Tutorial')

############  Command Specific error handling  #############
	@folderdm.error
	async def foldercmd_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.author.send('!folder requires a foldername!\nUsage: !folder foldername')
			channel_type = str(ctx.channel.type)			
			if channel_type != 'private':
				await ctx.message.delete()

	@luadm.error
	async def luacmd_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.author.send('!lua requires a filename!\nUsage: !lua filename \n Extension .lua is not required!')
			channel_type = str(ctx.channel.type)			
			if channel_type != 'private':
				await ctx.message.delete()

	@functiondm.error
	async def functioncmd_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.author.send('!function requires a functionname!\nUsage: !function functionname \n () or additional arguments are not required!')
			channel_type = str(ctx.channel.type)			
			if channel_type != 'private':
				await ctx.message.delete()



def setup(bot):
	bot.add_cog(Knowledgebase(bot))

