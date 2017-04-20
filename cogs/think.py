from discord.ext import commands
from random import choice
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import box
import discord
import time
import os
from os import listdir
from os.path import isfile, join
import asyncio
import re

DEFAULT_DIR = "./data/think/thinking"

thinkReg = re.compile(':th[aeiou]+nk\w*:', re.IGNORECASE)

class Think:
	"""Initialization function"""
	def __init__(self, bot):
		self.bot = bot
		self.thinks = getThinks(DEFAULT_DIR)
		if len(self.bot.servers) > 0:
			self.mainServer = list(self.bot.servers)[0]
	
	"""Posts a random think to the channel"""
	@commands.command(pass_context=True)
	async def randomThink(self, ctx):
		"""This returns a random thinking emote."""
		channel = ctx.message.channel
		await self.bot.send_file(channel, join(DEFAULT_DIR, choice(self.thinks)))
	
	async def on_message(self, message):
		"""This returns a random thinking emote when someone sends a message with 'think'."""
		if message.author.id != self.bot.user.id and (thinkReg.search(str(message.content).lower()) != None or "🤔" in str(message.content) or message.content.lower() == "think" or message.content.lower() == "thonk" or message.content.lower() == "thunk"):
			channel = message.channel
			await self.bot.send_file(channel, join(DEFAULT_DIR, choice(self.thinks)))
	
	async def on_reaction_add(self, reaction, user):
		if thinkReg.search(str(reaction.emoji).lower()) != None or "🤔" in str(reaction.emoji):
			await self.bot.add_reaction(reaction.message, reaction.emoji)
	
	async def on_ready(self):
		self.mainServer = list(self.bot.servers)[0]

def getThinks(mypath):
	return [f for f in listdir(mypath) if (isfile(join(mypath, f)) and not f.endswith('.db'))]

def setup(bot):
	bot.add_cog(Think(bot))